import discord
from discord.ext import commands

from discord_slash import cog_ext

from sys import path
from discord_slash.context import SlashContext

from discord_slash.utils.manage_commands import create_choice, create_option
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Error.permissions import *
from Error.nwc import nwc
from Error.inv_arg import *
from Error.sww import *

class SlowMode(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    def get_unit_text(self, unit):
        unit_text = ""
        if unit == 1:
            unit_text = "sec"
        elif unit == 60:
            unit_text = "min"
        else:
            unit_text = "h"
        return unit_text
    
    @cog_ext.cog_slash(
        name="slowmode",
        description="Slows things down in a text channel by a given time",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="amount",
                description="Provide a delay",
                required=True,
                option_type=4
            ),
            create_option(
                name="unit",
                description="Provide delay unit",
                required=True,
                option_type=3,
                choices=[
                    create_choice(name="second/s", value="1"),
                    create_choice(name="minute/s", value="60"),
                    create_choice(name="hour/s", value="3600")
                ]
            )
        ]
    )
    async def slowmode(self, ctx:SlashContext, amount:int, unit:str):
        if not (ctx.author.guild_permissions.manage_messages):
            return await permission_error(ctx, permissions=["manage_messages"])
        
        unit = int(unit)
        unit_text = self.get_unit_text(unit)

        if (amount < 0):
            amount = abs(amount)

        if (amount == 0 and ctx.channel.slowmode_delay == 0):
            return await nwc(ctx, f"```Channel's slowmode was not activated!```\n**Channel**: {ctx.channel.mention}\n**Reason**: The amount equals **0**")

        if not ((amount <= 21600 and unit == 1) or (amount <= 360 and unit == 60) or (amount <= 6 and unit == 3600)):
            return await inv_arg(ctx, "```Amount {}{} >= 6h(max)```".format(amount, unit_text))

        try:
            slowmode_time = amount * unit
            await ctx.channel.edit(slowmode_delay=slowmode_time)
            slowmode_delay = ctx.channel.slowmode_delay

            embed = discord.Embed(
                title="Slowmode Off :mobile_phone_off:" if slowmode_delay == 0 else "Slowmode On :snail:",
                description="```No slowmode delay in this channel!```" if amount == 0 else f"Set the slowmode delay in {ctx.channel.mention} to about **{amount}**{unit_text}!",
                color=discord.Color.dark_green()
            ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

            await ctx.reply(embed=embed)
            return increase_uses()

        except:
            return await sww(ctx, "")


def setup(client):
    client.add_cog(SlowMode(client))