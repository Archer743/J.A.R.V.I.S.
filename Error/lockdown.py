import discord

def channels_locked(ctx, locked_channels, all_channels):
    title = ""

    if locked_channels == 1:
        title = "Channel Locked :lock:"
    else:
        title = "Channels Locked :lock:"

    embed = discord.Embed(
        title=title,
        description=f"``{locked_channels}`` **out of** ``{all_channels}`` **text channels were locked!**",
        color=discord.Color.from_rgb(255,215,0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

    return embed

def channels_unlocked(ctx, unlocked_channels, all_channels):
    title = ""

    if unlocked_channels == 1:
        title = "Channel Unlocked :lock:"
    else:
        title = "Channels Unlocked :lock:"

    embed = discord.Embed(
        title=title,
        description=f"``{unlocked_channels}`` **out of** ``{all_channels}`` **text channels were unlocked!**",
        color=discord.Color.from_rgb(255,215,0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

    return embed