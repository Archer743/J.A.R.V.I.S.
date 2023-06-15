import discord
from discord.ext import commands
from discord_slash import cog_ext

from sys import path
from discord_slash.context import SlashContext

from discord_slash.utils.manage_commands import create_option
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Error.permissions import *


class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="clear",
        description="Deletes a given number of messages in a text channel",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="amount",
                description="Provide a number (under or equal to 100) of messages that will be deleted",
                required=False,
                option_type=4
            )
        ]
    )
    async def clear(self, ctx:SlashContext, amount=None):
        if not ctx.author.guild_permissions.manage_messages:
            return await permission_error(self.client, ctx, ["manage messages"])
        
        if amount == None:
            amount = 1
        elif amount == 0:
            error = discord.Embed(title="Nothing Was Deleted!", color=discord.Color.from_rgb(14, 39, 46)).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            return await ctx.reply(embed=error, delete_after=3)
        elif amount < 0:
            amount = abs(amount)

        if amount > 100:
            error = discord.Embed(title="Error :red_circle:",
                description=f"The amount must be a number under or equal to ***100***\n**Your Amount:** ***{amount}***",
                color=discord.Color.red()
            ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            return await ctx.reply(embed=error, delete_after=3)

        await ctx.channel.purge(limit=amount)
        
        embed = discord.Embed(
            title="Done :green_circle: ",
            description="You deleted ***{}*** {} in this channel.".format(amount, "**messages**" if amount >= 2 else "**message**"),
            color=discord.Color.dark_green()
        ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=embed, delete_after=3)
        return increase_uses()


def setup(client):
    client.add_cog(Clear(client))