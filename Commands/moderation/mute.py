import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option

import datetime
import asyncio

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Data.DB_commands.server_settings import *
from Error.permissions import *
from Error.mute import *
from Error.nwc import *
from Error.sww import *


class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="mute",
        description="Mutes a given member",
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
                description="Provide a reason",
                required=False,
                option_type=3
            )
        ]
    )
    async def mute(self, ctx:SlashContext, member:discord.Member, reason:str=None):
        if not (ctx.author.guild_permissions.manage_messages):
            return await permission_error(ctx, permissions=["manage_messages"])

        if member.id == self.client.user.id:
            return await mute(ctx, f"```I can't mute myself!```")
        
        if member.id == ctx.author.id:
            return await mute(ctx, f"```You can't mute yourself!```")
        
        if member.top_role >= ctx.author.top_role:
            return await higher_mute(ctx, member)

        try:
            reason = None if reason == None else reason[:512]
            mute_role = get_mute_role(ctx)

            if not mute_role:
                return await sww(ctx, "```Mute Role Not Found!```")

            if mute_role in member.roles:
                return await already_muted(ctx, member)
            
            await member.add_roles(mute_role, reason=reason)

            embed = discord.Embed(title="Mute :mute:", color=discord.Color.from_rgb(14, 39, 46)).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Member", value=f"```{member.name}```", inline=False)
            embed.add_field(name="Muted At", value="```{}```".format(datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M %p, UTC")), inline=False)
            embed.add_field(name="Reason", value="```{}```".format(reason), inline=False)

            await ctx.reply(embed=embed.set_thumbnail(url=member.avatar_url))

            if not member.bot:
                await member.send(embed=embed.set_thumbnail(url=ctx.guild.icon_url).add_field(name="Server", value=f"```{ctx.guild.name}```", inline=True))

            return increase_uses()
        except:
            client_member = ctx.guild.get_member(user_id=self.client.user.id) # gets client's top role
            sy = ">=" if member.top_role >= client_member.top_role else "<="
            return await mute(ctx, f"```{member.name}'s top role in the server is higher or equal to mine!```{member.top_role.mention} **{sy}** {client_member.top_role.mention}")


def setup(client):
    client.add_cog(Mute(client))