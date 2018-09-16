<<<<<<< HEAD
# Red - A multifunction Discord bot
#### *Fun bringer, admin helper and music bot*  
[<img align="right" title="Art by Supergiant Games" src="https://www.supergiantgames.com/static/images/transistor/cartoon_red.png">](https://www.supergiantgames.com/games/transistor/)

[<img src="https://img.shields.io/badge/Support-me!-orange.svg">](https://www.patreon.com/Twentysix26) [<img src="https://img.shields.io/badge/Official-Server-green.svg">](https://discord.gg/0k4npTwMvTpv9wrh) **< Announcements & Help!**  
##**[ [This version is obsolete and no longer being supported. Use the current one] ](https://github.com/Twentysix26/Red-DiscordBot/)**  
### Cool title, but what does it do exactly?
A bit of everything. Seriously though:  
It has the [most common features](#general-commands) of many chatbots (!flip, !8, stopwatch, etc.), **custom commands** (inspired by Twitch's [Nightbot](https://www.nightbot.tv/)), memes.  
It features some games such as **Trivia**, rock paper scissors, [users can earn and play with credits](#economy-commands) in the slot machine.  
[The audio part is quite fleshed out](#audio-commands). Users can **stream youtube videos**, create **playlists** that everyone will be able to play and control (previous/next song, pause/resume, shuffle...).  
**MP3 and flac files can also be streamed** (see [FAQ](#faq) for details on local playlists)  
**Twitch's online notifications**: Red will notify the channels you want whenever you favorite Twitch streamers are online.  
As for the moderation tools, it includes a **powerful message filter with regular expression capabilities** and **mass messages cleanup**.  
[I'm planning to expand all this much more](#todo-list).  
See the [command list](#general-commands) for an even better idea of what this bot can do.

### I don't even know what I'm looking at. How do I install this?
Do not panic. [Enter the wiki and follow the tutorials](https://github.com/Twentysix26/Red-DiscordBot/wiki)!  
If you have any issue, consult the [troubleshooting](https://github.com/Twentysix26/Red-DiscordBot/wiki/Troubleshooting) page, and if you're still stuck, [join the official server](https://discord.gg/0k4npTwMvTpv9wrh) so you can get some help.
Once you're done, take a look at the command list and have fun.

### General commands

| Command                                       | Description                                |
|-----------------------------------------------|--------------------------------------------|
| !flip                                         | Flip a coin                                |
| !rps [rock/paper/scissors]                    | Play  RPS                                  |
| !proverb                                      | Random proverb                             |
| !choose [option1 or option2 or option3 (...)] | Random choice. Supports multiple words     |
| !8 [question?]                                | Ask 8 ball a question                      |
| !sw                                           | Start/stop the stopwatch                   |
| !trivia                                       | Trivia help and lists                      |
| !trivia [list]                                | Start a trivia session                     |
| !trivia stop                                  | Stop a trivia session                      |
| !twitch [stream]                              | Check if stream is online                  |
| !twitchalert [stream]                         | Red sends an alert in the channel when the stream is online (admin only)|
| !stoptwitchalert [stream]                     | Stop stream alerts (admin only)      |
| !roll [number]                                | Random number between 0 and chosen number. |
| !gif [text]                                   | GIF search                                 |
| !imdb [movie/etc]                             | Retrieve information from IMDB             |
| !meme [id;text1;text2]                        | Create a meme                              |
| !poll [question;answer1;answer2 (...)]        | Start poll in the current channel          |
| !endpoll                                      | Stop poll                                  |
| !addcom [command] [text]                      | Add a custom command                       |
| !editcom [command] [text]                     | Edit a custom command                      |
| !delcom [command]                             | Delete a custom command                    |
| !customcommands                               | Custom commands' list                      |
| !help                                         | Command list                               |
| !audio help                                   | Audio command list and playlist explanation.|
| !economy                                      | Explanation of the economy module          |
| !admin help                                   | Admin commands list                        |
| !meme help                                    | Explanation of !meme                       |

### Audio commands

| Command                    | Description                                                         |
|----------------------------|---------------------------------------------------------------------|
| !youtube [link]            | Play a youtube video in a voice channel                             |
| !sing                      | Make Red sing                                                       |
| !stop                      | Stop any voice channel activity                                     |
| !play [playlist_name]      | Play chosen playlist                                                |
| !playlists                 | Playlist's list                                                     |
| !next or !skip             | Next song                                                           |
| !prev                      | Previous song                                                       |
| !pause                     | Pause song                                                          |
| !resume                    | Resume song                                                         |
| !replay or !repeat         | Replay current song                                                 |
| !title or !song            | Current song's title + link                                         |
| !shuffle                   | Mix current playlist                                                |
| !volume [0-1]              | Sets Red's output volume                                            |
| !addplaylist [name] [link] | Add a youtube playlist                                              |
| !delplaylist [name]        | Delete a youtube playlist. Limited to author and admins             |
| !getplaylist               | Get the current playlist through DM. This also works with favorites |
| !addfavorite               | Add song to your favorites                                          |
| !delfavorite               | Remove song from your favorites                                     |
| !playfavorites             | Play your favorites                                                 |
| !local [playlist_name]     | Play chosen local playlist                                          |
| !local or !locallist       | Local playlists' list                                               |
| !downloadmode              | Enables or disables download mode. (admin only)                     |

### Admin commands

| Command                                                   | Description                                       |
|-----------------------------------------------------------|---------------------------------------------------|
| !addwords [word1 word2 (...)] [phrase/with/many/words]    | Add words to message filter                       |
| !removewords [word1 word2 (...)] [phrase/with/many/words] | Remove words from message filter                  |
| !addregex [regex]                                         | Add regular expression to message filter          |
| !removeregex [regex]                                      | Remove regular expression from message filter     |
| !shutdown                                                 | Close the bot                                     |
| !join [invite]                                            | Join another server                               |
| !leaveserver                                              | Leave server                                      |
| !shush                                                    | Ignore the current channel                        |
| !talk                                                     | Stop ignoring the current channel                 |
| !reload                                                   | Reload most files. Useful in case of manual edits |
| !name [name]                                              | Change the bot's name                             |
| !cleanup [number]                                         | Delete the last [number] messages                 |
| !cleanup [name/mention] [number]                          | Delete the last [number] of messages by [name]    |
| !blacklist [name/mention]                                 | Add user to blacklist. Red will ignore that user  |
| !forgive [name/mention]                                   | Remove user from blacklist                        |
| !setting [setting] [value]                                | Modify setting                                    |


### Economy commands

| Command     | Description                          |
|-------------|--------------------------------------|
| !register   | Register a new account               |
| !balance    | Check your balance                   |
| !slot [bid] | Play the slot machine                |
| !slot help  | Slot machine explanation and payouts |
| !payday     | Receive credits                      |

### FAQ
>I've done everything the README asked me to and it still doesn't work! Were you drunk when you coded this?  

You're probably missing something.  
Feel free to join [my server](https://discord.gg/0k4npTwMvTpv9wrh) and head to #support to get some help! Oh, and my drinking habits are none of your business.  

>Does this bot work on multiple servers?  

Sure it does. Should you do it? Maybe. The permissions system is not that great at the moment but if you trust the people running the server it's ok. It's not advisable to send the bot in random servers at the moment.   
Custom commands only work in the server they were created in. Same for the message filter. This is by design. Also, remember that the bot can only be in one voice channel at once.

>Will you implement [feature]?  

Suggestions are always very welcome.

>How do local playlists work?

Make as many folders as you want inside the localtracks folder. Names must be without spaces. Every folder counts as a different playlist. Every playlist can contain mp3 and flac files. Users can stream them by doing !local [playlist_name] and see the full list
with !local or !locallist. They can also add tracks to their favorites.

>What's download mode?

Everytime you play the audio of a youtube video with download mode on the audio will be first downloaded and stored into the "cache" folder. It is recommended that you use this mode to avoid streaming problems. This is the default mode, you can switch between modes with !downloadmode.

>Why is this bot called Red and the admin role "Transistor"? What's the meaning of !sing?

They're all references to [Transistor](https://www.supergiantgames.com/games/transistor/), a videogame by Supergiant Games.

### TODO List
- [x] [Start rewriting Red](https://github.com/Twentysix26/Red-DiscordBot/tree/develop)
- [ ]  ~~Bundle some malware and slowly build up a botnet for world domination~~
=======
![intro](http://i.imgur.com/RgGlNpQ.jpg)

# Red - A fully customizable Discord bot
#### *Music, admin, trivia, fun commands and much more!*
[<img src="https://img.shields.io/badge/Support-Red!-orange.svg">](https://www.patreon.com/Red_Devs)  [<img src="https://img.shields.io/badge/discord-py-blue.svg">](https://github.com/Rapptz/discord.py) [<img src="https://discordapp.com/api/guilds/133049272517001216/widget.png?style=shield">](https://discord.gg/red) [![Build Status](https://api.travis-ci.org/Cog-Creators/Red-DiscordBot.svg?branch=develop)](https://travis-ci.org/Cog-Creators/Red-DiscordBot) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

**Red** is a fully modular bot – meaning all features and commands can be enabled/disabled to your liking, making it completely customizable.  
This is also a *self-hosted bot* – meaning you will need to host and maintain your own instance. You can turn Red into an admin bot, music bot, trivia bot, new best friend or all of these together!  
[Installation is easy](https://twentysix26.github.io/Red-Docs/), and you do NOT need to know anything about coding! Aside from installation and updating, every part of the bot can be controlled from within Discord.

The default set of modules includes and is not limited to:
* Moderation features (kick/ban/softban/hackban, mod-log, filter, chat cleanup)
* Trivia (lists are included and can be easily added)
* Music features (YouTube, SoundCloud, local files, playlists, queues)
* Stream alerts (Twitch, Mixer, Smashcast)
* Slot machines
* Custom commands
* Imgur/gif search

Additionally, other modules (cogs) can be easily found and added from our growing community of cog repositories. Including:
* Cleverbot integration (talk to Red and she talks back)
* Loggers
* Welcome messages setup
* Reminders
* Raffles
* Leveler (increase levels for server participation)
* Sound effects
* And much, much more!

Feel free to take a [peek](https://cogs.red/)!

# Installation

The installation process is straightforward; all major platforms are supported: 
* [Windows](https://twentysix26.github.io/Red-Docs/red_install_windows/)
* [Linux](https://twentysix26.github.io/Red-Docs/red_install_linux/)
* [macOS](https://twentysix26.github.io/Red-Docs/red_install_mac/)

Read the [getting started](https://twentysix26.github.io/Red-Docs/red_getting_started/) guide to quickly learn how to use Red.  

If you have any other questions, feel free to explore the [Docs](https://twentysix26.github.io/Red-Docs/) for guidance.

If [*after reading the guides*](https://twentysix26.github.io/Red-Docs/) you are still experiencing issues that are not listed on [this page](https://twentysix26.github.io/Red-Docs/red_guide_troubleshooting/) or in the [FAQs](https://twentysix26.github.io/Red-Docs/red_faq/), feel free to join the [official server](https://discord.gg/red) for help.  
Have fun!

# Join the community!

Red is in continuous development, and it’s supported by an active community which produces new content (cogs/plugins) for everyone to enjoy. New features are constantly added. If you can’t [find](https://cogs.red/) what you’re looking for, we are open to suggestions! Stay tuned by [joining the official server](https://discord.gg/red)!

# License

Released under the [GNU GPL v3](LICENSE).

*Red is named after the main character of "Transistor", a videogame by [Supergiant Games](https://www.supergiantgames.com/games/transistor/)*
>>>>>>> remotes/origin/develop
