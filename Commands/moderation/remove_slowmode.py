import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Error.permissions import *
from Error.sww import sww


class RemoveSlowmode(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="remove_slowmode",
        description="Removes slowmode delay in a text channel",
        guild_ids=[805867479909924905]
    )
    async def remove_slowmode(self, ctx:SlashContext):
        if not (ctx.author.guild_permissions.manage_messages):
            return await permission_error(ctx, permissions=["manage_messages"])
        
        try:
            slowmode_delay = ctx.channel.slowmode_delay

            embed = discord.Embed(
                title="Slowmode Off :mobile_phone_off:" if slowmode_delay != 0 else "Slowmode Already Off :mobile_phone_off:",
                description=f"Slowmode removed in {ctx.channel.mention}!" if slowmode_delay != 0 else "```No slowmode delay in this channel!```",
                color=discord.Color.dark_green()
            ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

            await ctx.channel.edit(slowmode_delay=0)
            await ctx.reply(embed=embed)
            return increase_uses()
        
        except:
            return await sww(ctx, "")


def setup(client):
    client.add_cog(RemoveSlowmode(client))