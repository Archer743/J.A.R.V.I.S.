import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from sys import path
path.insert(1, "../../Data")
from Data.DB_commands.bot_info import increase_uses

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="ping", description="Provides my latency", guild_ids=[805867479909924905])
    async def ping(self, ctx:SlashContext):
        embed = discord.Embed(
            title="Pong :ping_pong: ",
            description=f"Latency: **{round(self.client.latency * 1000)}**ms",
            color=discord.Color.from_rgb(14, 39, 46)
        )

        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        increase_uses()


def setup(client):
    client.add_cog(Ping(client))