import asyncio
from datetime import datetime, timedelta
import discord
import logging
import re
from time import time
from discord.ext import commands

from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from cogs.utils.chat_formatting import box, error, warning

__version__ = "1.5.0"

logger = logging.getLogger("red.gallery")

JSON = "data/gallerysettings.json"

POLL_INTERVAL = 5 * 60  # 5 minutes
PARALLEL_TASKS = 4

UNIT_TABLE = (
    (("weeks", "wks", "w"), 60 * 60 * 24 * 7),
    (("days", "dys", "d"), 60 * 60 * 24),
    (("hours", "hrs", "h"), 60 * 60),
    (("minutes", "mins", "m"), 60),
    (("seconds", "secs", "s"), 1),
)

DEFAULTS = {
    "ENABLED": False,
    "ARTIST_ROLE": "artist",
    "EXPIRATION": 60 * 60 * 24 * 2,  # 2 days
    "PIN_EMOTES": ["\N{ARTIST PALETTE}", "\N{PUSHPIN}"],
    "PRIV_ONLY": False,
    "PINS_ONLY": False,
}

RM_EMOTES = {"❌"}# Exceptions
class CleanupError(Exception):
    def __init__(self, channel, orig):
        self.channel = channel
        self.original = orig


class BadTimeExpr(ValueError):
    pass


def _find_unit(unit):
    for names, length in UNIT_TABLE:
        if any(n.startswith(unit) for n in names):
            return names, length
    raise BadTimeExpr("Invalid unit: %s" % unit)


def _parse_time(time):
    time = time.lower()
    if not time.isdigit():
        time = re.split(r"\s*([\d.]+\s*[^\d\s,;]*)(?:[,;\s]|and)*", time)
        time = sum(map(_timespec_sec, filter(None, time)))
    return int(time)


def _timespec_sec(expr):
    atoms = re.split(r"([\d.]+)\s*([^\d\s]*)", expr)
    atoms = list(filter(None, atoms))

    if len(atoms) > 2:  # This shouldn't ever happen
        raise BadTimeExpr("invalid expression: '%s'" % expr)
    elif len(atoms) == 2:
        names, length = _find_unit(atoms[1])
        if atoms[0].count(".") > 1 or not atoms[0].replace(".", "").isdigit():
            raise BadTimeExpr("Not a number: '%s'" % atoms[0])
    else:
        names, length = _find_unit("seconds")

    try:
        return float(atoms[0]) * length
    except ValueError:
        raise BadTimeExpr("invalid value: '%s'" % atoms[0])


def _generate_timespec(sec, short=False, micro=False):
    timespec = []

    for names, length in UNIT_TABLE:
        n, sec = divmod(sec, length)

        if n:
            if micro:
                s = "%d%s" % (n, names[2])
            elif short:
                s = "%d%s" % (n, names[1])
            else:
                s = "%d %s" % (n, names[0])
            if n <= 1:
                s = s.rstrip("s")
            timespec.append(s)

    if len(timespec) > 1:
        if micro:
            return "".join(timespec)

        segments = timespec[:-1], timespec[-1:]
        return " and ".join(", ".join(x) for x in segments)

    return timespec[0]


async def _sem_wrapper(semaphore, task):
    async with semaphore:
        return await task


class Gallery:
    """Message auto-deletion for gallery channels"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(JSON)
        self._task = bot.loop.create_task(self.loop_task())
        self._semaphore = asyncio.Semaphore(PARALLEL_TASKS)

        try:
            self.analytics = CogAnalytics(self)
        except Exception as error:
            self.bot.logger.exception(error)
            self.analytics = None

    def __unload(self):
        self._task.cancel()

    def save(self):
        dataIO.save_json(JSON, self.settings)

    def settings_for(self, channel: discord.Channel) -> dict:
        cid = channel.id
        if cid not in self.settings:
            return DEFAULTS
        return self.settings[cid]

    def update_setting(self, channel: discord.Channel, key: str, val) -> None:
        cid = channel.id
        if cid not in self.settings:
            self.settings[cid] = DEFAULTS
        self.settings[cid][key] = val
        self.save()

    def enabled_in(self, chan: discord.Channel) -> bool:
        return chan.id in self.settings and self.settings[chan.id]["ENABLED"]

    def get_message_check(self, channel: discord.Channel, settings: dict = None):
        assert self.enabled_in(channel)

        if settings is None:
            settings = self.settings_for(channel)

        server = channel.server
        settings = self.settings_for(channel)
        priv_only = settings.get("PRIV_ONLY", False)
        pins_only = settings.get("PINS_ONLY", False)

        mod_role = self.bot.settings.get_server_mod(server).lower()
        admin_role = self.bot.settings.get_server_admin(server).lower()
        artist_role = settings["ARTIST_ROLE"].lower()
        admin_roles = {mod_role, admin_role}
        priv_roles = admin_roles.union([artist_role])

        admins = {}
        privs = {}

        pin_emojis = set(settings["PIN_EMOTES"])
        valid_emojis = pin_emojis | RM_EMOTES

        async def message_check(message: discord.Message) -> bool:
            author = message.author
            privileged = privs.get(author.id)

            if isinstance(author, discord.Member) and privileged is None:
                privileged = privs[author.id] = any(r.name.lower() in priv_roles for r in author.roles)

            has_content = message.attachments or message.embeds

            e_pin = pin_emojis.intersection(message.content or "")
            r_pin = False
            x_pin = False

            for reaction in message.reactions:
                if reaction.emoji not in valid_emojis or x_pin:
                    continue
                elif (reaction.emoji in pin_emojis) and (r_pin or message.pinned or (e_pin and privileged)):
                    continue

                users = await self.bot.get_reaction_users(reaction)

                for user in users:
                    member = server.get_member(user.id)

                    if not member:
                        continue

                    if reaction.emoji in RM_EMOTES and not x_pin:
                        x_pin |= admins.get(member.id, False)

                        if not x_pin:
                            is_admin = admins[member.id] = any(r.name.lower() in admin_roles for r in member.roles)

                            if is_admin:
                                privs[member.id] = True
                                x_pin = is_admin
                    elif not r_pin:
                        r_pin |= privs.get(member.id, False)

                        if not r_pin:
                            is_priv = privs[member.id] = any(r.name.lower() in priv_roles for r in member.roles)
                            r_pin |= is_priv

            pinned = r_pin or message.pinned or (e_pin and privileged)  # All three ways a message can be "pinned"
            content_keep = has_content and not pins_only  # pins_only overrides presence of content
            keep = content_keep and not (priv_only and not privileged)  # priv_only also overrides presence of content
            return x_pin or not (pinned or keep)  # x_pin overrides both pinned and keep

        return message_check

    async def cleanup_task(self, channel: discord.Channel) -> None:
        try:
            to_delete = []
            settings = self.settings_for(channel)
            now = datetime.utcnow()
            before = now - timedelta(seconds=settings["EXPIRATION"])
            after = now - timedelta(days=14, seconds=-30)

            check = self.get_message_check(channel, settings=settings)

            while True:
                async for message in self.bot.logs_from(channel, before=before, after=after):
                    before = message
                    if await check(message):
                        to_delete.append(message)
                else:
                    break

            while to_delete and to_delete[-1].timestamp < after:
                to_delete.pop()

            if to_delete:
                await self.mass_purge(to_delete)
        except Exception as e:
            raise CleanupError(channel, e)

    async def loop_task(self):
        try:
            while True:
                await self.bot.wait_until_ready()  # bot may become un-ready
                start = time()
                tasks = []

                for cid, d in self.settings.items():
                    if not d["ENABLED"]:
                        continue

                    channel = self.bot.get_channel(cid)

                    if not (channel and channel.server):
                        logger.warning("Attempted to curate missing channel ID #%s." % cid)
                        continue

                    perms = channel.permissions_for(channel.server.me)

                    if not (perms.read_message_history and perms.read_messages and perms.manage_messages):
                        logger.warning("Missing permissions to read or manage messages in channel ID #%s." % cid)
                        continue

                    tasks.append(_sem_wrapper(self._semaphore, self.cleanup_task(channel)))

                results = await asyncio.gather(*tasks, return_exceptions=True)

                for res in results:
                    if isinstance(res, CleanupError):
                        logger.exception(
                            "Exception cleaning in %s #%s:" % (res.channel.server, res.channel), exc_info=res.original
                        )

                remaining = POLL_INTERVAL - (time() - start)
                if remaining > 0:
                    await asyncio.sleep(remaining)

        except asyncio.CancelledError:
            pass

    @commands.group(pass_context=True, allow_dm=False)
    @checks.mod_or_permissions(manage_messages=True)
    async def galset(self, ctx):
        """
        Gallery module settings
        """
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
            if ctx.message.channel.id not in self.settings:
                await self.bot.say("Settings for %s: not configured." % ctx.message.channel.mention)
                return

            settings = self.settings_for(ctx.message.channel)
            await self.bot.say(("Settings for %s:\n" % ctx.message.channel.mention)
                + box("\n".join((
                    "Enabled          : " + ("yes" if settings["ENABLED"] else "no"),
                    "Artist role name : " + (settings["ARTIST_ROLE"] or "(not set)"),
                    "Max message age  : " + _generate_timespec(settings["EXPIRATION"]),
                    "Pin emojis       : " + ", ".join(settings.get("PIN_EMOTES", [])),
                    "Pins only        : " + ("yes" if settings.get("PINS_ONLY") else "no"),
                    "Privileged only  : " + ("yes" if settings.get("PRIV_ONLY") else "no"),
                )))
            )

    @galset.command(pass_context=True, allow_dm=False)
    async def emotes(self, ctx, *emotes):
        """
        Show or update the emotes used to indicate artwork
        """
        channel = ctx.message.channel

        if not emotes:
            em = self.settings_for(channel)["PIN_EMOTES"]
            await self.bot.say("Pin emotes for this channel: " + " ".join(em))
        else:
            if any(len(x) != 1 for x in emotes):
                await self.bot.say("Error: You can only use unicode emotes.")
                return

            self.update_setting(channel, "PIN_EMOTES", emotes)
            await self.bot.say("Updated pin emotes for this channel.")

    @galset.command(pass_context=True, allow_dm=False)
    async def turn(self, ctx, on_off: bool = None):
        """
        Turn gallery message curation on or off
        """
        channel = ctx.message.channel
        current = self.settings_for(channel)["ENABLED"]
        perms = channel.permissions_for(channel.server.me).manage_messages
        adj_bool = current if on_off is None else on_off
        adj = "enabled" if adj_bool else "disabled"

        if on_off is None:
            await self.bot.say("Gallery cog is %s in this channel." % adj)
        else:
            if self.enabled_in(channel) == on_off:
                await self.bot.say("Already %s." % adj)
            else:
                if on_off and not perms:
                    await self.bot.say('I need the "Manage messages" permission in this channel to work.')
                    return

                self.update_setting(channel, "ENABLED", on_off)
                await self.bot.say("Gallery curation %s." % adj)

    @galset.command(pass_context=True, allow_dm=False)
    async def privonly(self, ctx, on_off: bool = None):
        """
        Set whether only privileged users' messages are kept

        Moderators, admins, and the artist role are considered privileged.

        If disabled (the default), all attachments and embeds are kept.
        """
        channel = ctx.message.channel
        current = self.settings_for(channel).get("PRIV_ONLY", False)

        if on_off is None:
            adj = "Currently,"
            on_off = current
        elif current == on_off:
            adj = "No change:"
        else:
            adj = "Updated:"
            self.update_setting(channel, "PRIV_ONLY", on_off)

        msg = "%s content posted by %s will be kept." % (adj, "privileged users" if on_off else "anyone")
        await self.bot.say(msg)

    @galset.command(pass_context=True, allow_dm=False)
    async def pinsonly(self, ctx, on_off: bool = None):
        """
        Set whether only pinned messages are kept

        Messages containing the configured emotes in their text, or with a
        reaction of any of the emotes by a mod or admin, are considered pinned.

        If disabled (default), all attachments and embeds are kept.
        """
        channel = ctx.message.channel
        current = self.settings_for(channel).get("PINS_ONLY", False)

        if on_off is None:
            adj = "Currently,"
            on_off = current
        elif current == on_off:
            adj = "No change:"
        else:
            adj = "Updated:"
            self.update_setting(channel, "PINS_ONLY", on_off)

        msg = "%s %s will be kept." % (adj, "only pinned messages" if on_off else "all messages with content")
        await self.bot.say(msg)

    @galset.command(pass_context=True, allow_dm=False)
    async def age(self, ctx, *, timespec: str = None):
        """
        Set the maximum age of non-art posts
        """
        channel = ctx.message.channel

        if not timespec:
            sec = self.settings_for(channel)["EXPIRATION"]
            await self.bot.say("Current maximum age is %s." % _generate_timespec(sec))
        else:
            try:
                sec = _parse_time(timespec)
            except BadTimeExpr as e:
                await self.bot.say(error(e.args[0]))
                return

            if sec >= (14 * 24 * 60 * 60):
                await self.bot.say(error(
                    "Discord limits bulk deletes to messages posted within two weeks. "
                    "Please choose a maximum age shorter than that."
                ))
                return

            self.update_setting(channel, "EXPIRATION", sec)
            msg = "Maximum post age set to %s." % _generate_timespec(sec)

            if sec < POLL_INTERVAL:
                poll_spec = _generate_timespec(POLL_INTERVAL)
                msg += "\n\n" + warning("Note: this cog only checks message history every %s." % poll_spec)

            await self.bot.say(msg)

    @galset.command(pass_context=True, allow_dm=False)
    async def role(self, ctx, role: discord.Role = None):
        """
        Sets the artist role
        """
        channel = ctx.message.channel

        if role is None:
            role = self.settings_for(channel)["ARTIST_ROLE"]
            await self.bot.say("Artist role name is currently %s." % role)
        else:
            self.update_setting(channel, "ARTIST_ROLE", role.name)
            await self.bot.say("Artist role set.")

    # Stolen from mod.py
    async def mass_purge(self, messages):
        while messages:
            if len(messages) > 1:
                await self.bot.delete_messages(messages[:100])
                messages = messages[100:]
            else:
                await self.bot.delete_message(messages[0])
                messages = []
            await asyncio.sleep(1)

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)

    async def on_channel_delete(self, channel):
        if self.settings.pop(channel.id, None) is not None:
            self.save()


def check_files():
    if not dataIO.is_valid_json(JSON):
        print("Creating empty %s" % JSON)
        dataIO.save_json(JSON, {})


def setup(bot):
    check_files()
    bot.add_cog(Gallery(bot))
