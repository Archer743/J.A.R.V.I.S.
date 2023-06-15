import discord

async def inv_arg(ctx, text:str):
    embed = discord.Embed(
        title="Invalid Argument!",
        description=text,
        color = discord.Color.from_rgb(204, 0, 0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

    return await ctx.reply(embed=embed)