import discord, datetime
from discord.ext import commands, tasks

from itertools import cycle
from termcolor import colored

from sys import path
path.insert(1, "../Data")

from Data.databases import *
from Data.DB_commands.server_settings import *
from Data.DB_commands.bot_info import get_uses, get_commands_number


class On_Ready(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.commands = get_commands_number()
        self.cur_status = cycle([0, 1])
    
    async def message(self):
        print(colored("===================", "red") + "BOT" + colored("============================", "red"))
        print(colored('Bot ', "magenta") + colored('{0.user}'.format(self.client), "red") + colored(' is ready!', "magenta"))
        print(colored("==================================================", "red"))

        embed = discord.Embed(
            title=f"{self.client.user.name} is online! :clapper:",
            description="**Date** :alarm_clock:```{}```".format(datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M:%S %p, UTC")),
            color=discord.Color.dark_green()
        ).set_thumbnail(url=self.client.user.avatar_url)

        guild = discord.utils.get(self.client.guilds, id=873915360695427073) # in J.A.R.V.I.S. HQ
        if guild:
            channel = discord.utils.get(guild.channels, id=926124379857903666) # online channel
            return await channel.send(embed=embed)

    @tasks.loop(seconds=30)
    async def change_status(self):
        users = 0
        for server in self.client.guilds:
            users += server.member_count
        
        stats = [
            f"on {len(self.client.guilds)} servers | {users} users",
            f"with {self.commands} commands | {get_uses()} times used"
        ] #(open('./z_others/stats.txt').read()).split('\n')

        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(stats[next(self.cur_status)]))

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        await self.message()


def setup(client):
    client.add_cog(On_Ready(client))