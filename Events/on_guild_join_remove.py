import discord
from discord.ext import commands

from sys import path
path.insert(1, "../Data")

from Data.databases import *


class On_Guild_Join_Remove(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guild_post = {
            "_id" : guild.id,
            "name" : guild.name,
            "prefix" : "-",
            "profanity" : False,
            "w_a_g_c" : None, # welcome_and_goodbye_channel =>w_a_g_c
            "hi_and_bye_mode" : False,
            "mute_role" : None
        }
        prefix_collection.insert_one(guild_post)
        #pass
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        prefix_collection.delete_one({"_id" : guild.id})
        #pass


# Connects this functionality to the bot
def setup(client):
    client.add_cog(On_Guild_Join_Remove(client))