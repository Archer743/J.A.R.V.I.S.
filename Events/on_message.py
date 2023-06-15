import discord
from discord.ext import commands
from profanity import profanity

from sys import path
path.insert(1, "../Data")

from Data.databases import *
from Data.DB_commands.server_settings import *


class On_Message(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        try:
            if (get_profanity(msg) == True) and profanity.contains_profanity(msg.content):
                await msg.delete()
                embed = discord.Embed(title="Bad Language :face_with_symbols_over_mouth:", description="You can't use bad words here!", color=discord.Color.red())
                await msg.channel.send(embed=embed, delete_after=10)
        except:
            pass
        
        try:
            if msg.mentions[0] == self.client.user:
                embed = discord.Embed(
                    title='Help :helmet_with_cross:',
                    description=f"Use **/** and find out my commands!",
                    color=discord.Color.from_rgb(14, 39, 46)
                )
                await msg.channel.send(embed=embed)
        except:
            pass
        
        #await self.client.process_commands(msg)


# Connects this functionality to the bot
def setup(client):
    client.add_cog(On_Message(client))