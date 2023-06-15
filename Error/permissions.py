import discord

async def permission_error(ctx, permissions:list):
    error = discord.Embed(
        title="Must Have Permissions" if len(permissions) >= 2 else "Must Have Permission",
        description="".join(f"```{permission}```" for permission in permissions),
        color=discord.Color.from_rgb(204, 0, 0)
    ).set_author(
        name=ctx.author,
        icon_url=ctx.author.avatar_url
    )

    return await ctx.reply(embed = error)