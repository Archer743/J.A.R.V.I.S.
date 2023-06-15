#nothing was changed

import discord

async def nwc(ctx, text):
    embed = discord.Embed(
        title="Nothing Was Changed!",
        description=text,
        color = discord.Color.from_rgb(204, 0, 0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

    return await ctx.reply(embed=embed)

def nwc_embed(ctx, text):
    embed = discord.Embed(
        title="Nothing Was Changed!",
        description=text,
        color = discord.Color.from_rgb(204, 0, 0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    
    return embed