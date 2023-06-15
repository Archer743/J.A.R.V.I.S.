import discord

async def kick(ctx, text):
    embed = discord.Embed(
        title="No One Was Kicked!", #Something Went Wrong!
        description=text,
        color=discord.Color.from_rgb(204, 0, 0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

    return await ctx.reply(embed=embed)

async def higher_kick(ctx, member:discord.Member):
    embed = discord.Embed(
        title="No One Was Kicked!", #Something Went Wrong!
        color=discord.Color.from_rgb(204, 0, 0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url).add_field(
        name="Member", value=f"{member.mention}", inline=True).add_field(
        name="Kicker", value=f"{ctx.author.mention}", inline=True).add_field(
        name="Reason", value="```You have a lower or equal top role in the role hierarchy compared to this user!```", inline=False)

    return await ctx.reply(embed=embed)