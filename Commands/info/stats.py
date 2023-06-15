import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext

import datetime, time

from sys import path
path.insert(1, "../../Data")
from Data.DB_commands.bot_info import *

import json
with open('./Data/config.json') as file:
    data = json.load(file)


class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="stats", description="Provides my statistics", guild_ids=[805867479909924905])
    async def stats(self, ctx:SlashContext):
        startTime, started = get_start_time()
        uptime = datetime.timedelta(seconds=int(round(time.time() - startTime)))

        users = 0
        channels = 0

        for server in self.client.guilds:
            users += server.member_count
            channels += len(server.channels)
   
        
        embed = discord.Embed(title="Statistics :bar_chart: ", color=discord.Color.from_rgb(14, 39, 46))

        embed.add_field(name='Name', value=f"```{self.client.user.name}```", inline=True)
        embed.add_field(name='Commands', value=f'```{get_commands_number()}```', inline=True)
        embed.add_field(name='Ping', value=f"```{round(self.client.latency * 1000)}ms```")

        embed.add_field(name='Servers', value=f"```{len(self.client.guilds)}```", inline=True)
        embed.add_field(name='Channels', value=f'```{channels}```', inline=True)
        embed.add_field(name='Users', value=f'```{users}```', inline=True)
        
        embed.add_field(name='Last Restart Date', value=f'```{started}```', inline=True)
                                                        #started_text
        
        embed.add_field(name='ID', value=f'```{self.client.user.id}```', inline=True)
        embed.add_field(name='Uptime', value=f'```{uptime}```', inline=True)
        embed.add_field(name='Commands Use', value=f'```{get_uses()} times used```', inline=True)
        embed.add_field(name='In Voice Channel?', value='```{}```'.format("Yes" if ctx.guild.me.voice != None else "No"), inline=True)
        embed.add_field(name='Extra Help', value=f'[Help Server]({data["help_server_link"]})', inline=True)

        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        increase_uses()
        return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Stats(client))