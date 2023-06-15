import discord
from reactionmenu import ReactionMenu
import datetime

async def mute(ctx, text):
    embed = discord.Embed(
        title="No One Was Muted!", #Something Went Wrong!
        description=text,
        color=discord.Color.from_rgb(204, 0, 0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    
    return await ctx.reply(embed=embed)

async def mute_role_not_found(ctx):
    error = discord.Embed(
        title="Mute Role Not Found!",
        color=discord.Color.from_rgb(204, 0, 0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    
    return await ctx.reply(embed=error)

async def higher_mute(ctx, member:discord.Member):
    error = discord.Embed(
        title="No One Was Muted!", #Something Went Wrong!
        color=discord.Color.from_rgb(204, 0, 0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url).add_field(
        name="Member", value=f"{member.mention}", inline=True).add_field(
        name="Muter", value=f"{ctx.author.mention}", inline=True).add_field(
        name="Reason", value="```You have a lower or equal top role in the role hierarchy compared to this user!```", inline=False)

    return await ctx.reply(embed=error)

async def already_muted(ctx, member:discord.Member):
    embed = discord.Embed(
        title="Member Muted!", #Something Went Wrong!
        description=f"{member.mention} is already muted!",
        color=discord.Color.from_rgb(204, 0, 0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    
    return await ctx.reply(embed=embed)

async def unmute(ctx, text):
    embed = discord.Embed(
        title="No One Was Unmuted!", #Something Went Wrong!
        description=text,
        color=discord.Color.from_rgb(204, 0, 0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    
    return await ctx.reply(embed=embed)

async def unmuted(ctx, member:discord.Member, mute_role:discord.Role):
    embed = discord.Embed(
        title="No One Was Unmuted!", #Something Went Wrong!
        description=f"{member.mention} doesn't have the server mute role {mute_role.mention}",
        color=discord.Color.from_rgb(204, 0, 0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    
    return await ctx.reply(embed=embed)

async def mute_role_created(ctx, role:discord.Role, perms:list):
    menu = ReactionMenu(ctx, back_button="⬅️", next_button="➡️", config=ReactionMenu.STATIC, timeout=120.0)
    
    page1 = discord.Embed(
        title="Mute Role Created :tools:",
        color=discord.Color.dark_green()
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    page1.add_field(name="Role", value=f"{role.mention}", inline=True)
    page1.add_field(name="Created At", value="```{}```".format(datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M %p, UTC")), inline=True)

    page2 = discord.Embed(
        title="Permissions :pencil:",
        description="".join(f"```{perm}```" for perm in perms),
        color=discord.Color.dark_green()
    )

    menu.add_page(page1)
    menu.add_page(page2)

    await menu.start()