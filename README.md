# Jarvis V 3.0

## Into
> This is a Discord bot that is designed to facilitate moderation, provide information about channels and users, and offer entertainment through a wide range of commands (a total of 30).

## Features
>  - slash commands
>
>  - file structure changed
>
>  - new functions added: see_settings, set_up, etc.
>
>  - DB commands placed in groups of files

## Modules
> - discord.py / nextcord
>
> - discord_slash
>
> - pymongo
>
> - reactionmenu
>
> - PyNaCl
>
> - *[ffmpeg](https://www.wikihow.com/Install-FFmpeg-on-Windows)*

## Commands: 30 / ~65
>
> | **Command Name**  | **Description** | **Arguments** |
> | :-------------: |:----------------------------------------:| :----------:|
> | `/add_role`    | **Adds a specific server role to a member** | *member, role*|
> | `/ban`     | **Given member of this server is banned from it**| *member, reason*|
> | `/channel_info` | **Provides information about a channel**      |    *channel*      |
> | `/clear` | **Deletes a given number of messages in a text channel** | *amount* |
> | `/cr_mute_role` | **Creates a mute role for your server** | *name, set_as_server_mute_role* |
> | `/die` | **Returns a random number from a die** | *None* |
> | `/emoji_info` | **Pass in one server emoji and receive its information** | *emoji* |
> | `/inspire` | **Gives you a wise thought of a famous person** | *None* |
> | `/invite` | **Provides my invite links** | *None* |
> | `/join` | **Adds me to your current voice channel** | *None* |
> | `/kick` | **Given member of this server is kicked from it** | *member, reason* |
> | `/leave` | **Disconnects me from my current voice channel** | *None* |
> | `/lockdown` | **Locks a given text channel** | *channel, all* |
> | `/mute` | **Mutes a given member** | *member, reason* |
> | `/nick` | **Changes member's nick in this server** | *member, nick* |
> | `/ping` | **Provides my latency** | *None* |
> | `/play` | **You give me a song, and I play it (Supports YouTube links)** | *song* |
> | `/profanity` | **See a change my anti-profanity mode for this server** | *option, toggle* |
> | `/profile` | **Provides member's info** | *type, member* |
> | `/random_int` | **Returns a random integer** | *min, max* |
> | `/remove_slowmode` | **Removes slowmode delay in a text channel** | *None* |
> | `/reset_nick` | **Resets member's nickname in this server** | *member* |
> | `/role_info` | **Provides information about a role** | *role* |
> | `/see_settings` | **See my settings for this server** | *None* |
> | `/server_info` | **Provides information about this server** | *None* |
> | `/setup` | **Sets everything that will be needed in my future work** | *w_a_g_m, w_a_g_c, profanity, mute_role* |
> | `/slowmode` | **Slows things down in a text channel by a given time** | *amount, unit* |
> | `/stats` | **Provides my statistics** | *None* |
> | `/take_role` | **Removes a specific serer role to a member** | *member, role* |
> | `/toss_coin` | **Try to guess the side of the coin** | *side* |
> | `/unban` | **Given member of this server is unbanned from it** | *user, reason* |
> | `/unlock` | **Unlocks a given text channel if its at lockdown** | *channel, all* |
> | `/unmute` | **Unmutes a muted member** | *member, reason* |
