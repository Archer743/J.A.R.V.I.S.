# something went wrong

import discord

async def sww(ctx, text):
    error = discord.Embed(
        title="Something Went Wrong!", #Something Went Wrong!
        description=text,
        color=discord.Color.from_rgb(204, 0, 0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    
    return await ctx.reply(embed=error)