import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option

import datetime

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Error.permissions import permission_error
from Error.kick import *


class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="kick",
        description="Given member of this server is kicked from it",
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
                description="What's the reason for kicking this user?",
                required=False,
                option_type=3
            )
        ]
    )
    async def kick(self, ctx:SlashContext, member:discord.Member, reason:str=None):
        if not (ctx.author.guild_permissions.manage_roles and ctx.author.guild_permissions.kick_members):
            return await permission_error(self.client, ctx, permissions=["manage_roles", "kick_members"])

        if member.id == self.client.user.id:
            return await kick(ctx, f"```I can't kick myself!```")
        
        if member.id == ctx.author.id:
            return await kick(ctx, f"```You can't kick yourself!```")

        if member.top_role >= ctx.author.top_role:
            return await higher_kick(ctx, member)

        try:
            reason = None if reason == None else reason[:512]
            await member.kick(reason=reason)

            embed = discord.Embed(title="Kick :gloves:", color=discord.Color.from_rgb(14, 39, 46)).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Member", value=f"```{member.name}```", inline=False)
            embed.add_field(name="Kicked At", value="```{}```".format(datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M %p, UTC")), inline=False)
            embed.add_field(name="Reason", value="```{}```".format(reason), inline=False)

            await ctx.reply(embed=embed.set_thumbnail(url=member.avatar_url))
            
            if not member.bot:
                await member.send(embed=embed.set_thumbnail(url=ctx.guild.icon_url).add_field(name="Server", value=f"```{ctx.guild.name}```", inline=True))
            return increase_uses()
            
        except:
            client_member = ctx.guild.get_member(user_id=self.client.user.id) # gets client's top role
            sy = ">=" if member.top_role >= client_member.top_role else "<="
            return await kick(ctx, f"```{member.name}'s top role in the server is higher or equal to mine!```{member.top_role.mention} **{sy}** {client_member.top_role.mention}")


def setup(client):
    client.add_cog(Kick(client))