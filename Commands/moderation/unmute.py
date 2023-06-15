import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Data.DB_commands.server_settings import *
from Error.permissions import *
from Error.sww import *
from Error.mute import *


class Unmute(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_slash(
        name="unmute",
        description="Unmutes a muted member",
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
    async def unmute(self, ctx:SlashContext, member:discord.Member, reason:str=None):
        if not(ctx.author.guild_permissions.manage_messages):
            return await permission_error(ctx, permissions=["manage_messages"])
        
        if not(get_mute_role(ctx)):
            return await mute_role_not_found(ctx)
        
        try:
            mute_role = get_mute_role(ctx)
            reason = None if reason == None else reason[:512]
            if mute_role not in member.roles:
                return await unmuted(ctx, member, mute_role)
            
            await member.remove_roles(mute_role, reason=reason)
            
            embed = discord.Embed(title="Unmute :speaker:", color=discord.Color.from_rgb(14, 39, 46)).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Member", value=f"```{member.name}```", inline=False)
            embed.add_field(name="Unmuted At", value="```{}```".format(datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M %p, UTC")), inline=False)
            embed.add_field(name="Reason", value="```{}```".format(reason), inline=False)

            await ctx.reply(embed=embed.set_thumbnail(url=member.avatar_url))

            if not member.bot:
                await member.send(embed=embed.set_thumbnail(url=ctx.guild.icon_url).add_field(name="Server", value=f"```{ctx.guild.name}```", inline=True))

            return increase_uses()

        except:
            return await sww(ctx, "")


def setup(client):
    client.add_cog(Unmute(client))