import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

import random

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")
from Data.DB_commands.bot_info import increase_uses


class Random(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="random_int",
        description="Returns a random integer",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="min",
                description="Min value",
                required=False,
                option_type=4
            ),
            create_option(
                name="max",
                description="Max value",
                required=False,
                option_type=4
            )
        ]
    )
    async def random_int(self, ctx:SlashContext, min:int=1, max:int=10):
        if min > max:
            temp = min
            min = max
            max = temp
        
        embed = discord.Embed(
            title="Random Number Generator :game_die:",
            color=discord.Color.random()
        ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        embed.add_field(name="MIN", value=f"**```{min}```**", inline=True)
        embed.add_field(name="RESULT", value=f"**```{random.randint(min, max)}```**", inline=True)
        embed.add_field(name="MAX", value=f"**```{max}```**", inline=True)

        await ctx.reply(embed=embed)
        return increase_uses()

    @cog_ext.cog_slash(
        name="toss_coin",
        description="Try to guess the side of the coin",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="side",
                description="Provide a side",
                option_type=4,
                required=True,
                choices=[
                    create_choice(name="Obverse", value=0),
                    create_choice(name="Reverse", value=1)
                ]
            )
        ]
    )
    async def toss_coin(self, ctx:SlashContext, side:int):
        embed = discord.Embed(
            title="Toss A Coin :coin:"
        ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        coin_side = random.randint(0, 1)

        if coin_side == side:
            embed.color = discord.Color.from_rgb(16, 119, 26) # Green
            embed.description = "***```Side Guessed!```***"
        else:
            embed.color = discord.Color.from_rgb(204, 0, 0)# Red
            embed.description = "***```Side Not Guessed!```***"

        await ctx.reply(embed=embed)
        return increase_uses()

    @cog_ext.cog_slash(name="die", description="Returns a random number from a die", guild_ids=[805867479909924905])
    async def die(self, ctx:SlashContext):
        embed = discord.Embed(
            title="Die :game_die:",
            description=f"**```{random.randint(1, 6)}```**",
            color=discord.Color.orange()
        ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=embed)
        return increase_uses()

def setup(client):
    client.add_cog(Random(client))