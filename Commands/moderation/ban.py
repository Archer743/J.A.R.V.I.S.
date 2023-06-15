import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from discord_slash.context import SlashContext

import datetime

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Error.permissions import *
from Error.ban import *


class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="ban",
        description="Given member of this server is banned from it",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="member",
                description="Provide a member",
                required=True,
                option_type=6
            ),
            create_option(
                name="reason",
                description="What's the reason for banning this user?",
                required=False,
                option_type=3
            )
        ]
    )
    async def ban(self, ctx:SlashContext, member:discord.Member, reason:str=None):
        if not (ctx.author.guild_permissions.ban_members and ctx.author.guild_permissions.manage_roles):
            return await permission_error(ctx, permissions=["ban_members", "manage_roles"])
        
        if member.id == self.client.user.id:
            return await ban(ctx, f"```I can't ban myself!```")
        
        if member.id == ctx.author.id:
            return await ban(ctx, f"```You can't ban yourself!```")

        if member.top_role >= ctx.author.top_role:
            return await higher_ban(ctx, member)

        try:
            reason = None if reason == None else reason[:512]
            await member.ban(reason=reason)

            embed = discord.Embed(title="Ban :hammer:", color=discord.Color.from_rgb(14, 39, 46)).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Member", value=f"```{member.name}```", inline=False)
            embed.add_field(name="Banned At", value="```{}```".format(datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M %p, UTC")), inline=False)
            embed.add_field(name="Reason", value="```{}```".format(reason), inline=False)

            await ctx.reply(embed=embed.set_thumbnail(url=member.avatar_url))
            
            if not member.bot:
                await member.send(embed=embed.set_thumbnail(url=ctx.guild.icon_url).add_field(name="Server", value=f"```{ctx.guild.name}```", inline=True))
            return increase_uses()
            
        except:
            client_member = ctx.guild.get_member(user_id=self.client.user.id) # gets client's top role
            sy = ">=" if member.top_role >= client_member.top_role else "<="
            return await ban(ctx, f"```{member.name}'s top role in the server is higher or equal to mine!```{member.top_role.mention} **{sy}** {client_member.top_role.mention}")


def setup(client):
    client.add_cog(Ban(client))