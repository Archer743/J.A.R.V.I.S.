import discord
from discord.ext import commands

from sys import path
path.insert(1, "../Data")
from Data.DB_commands.server_settings import *


class On_Guild_Role_Delete(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role:discord.Role):
        # role is seen as ctx here
        mute_role_id = get_mute_role_id(role)
        if mute_role_id == role.id:
            update_mute_role(role)


def setup(client):
    client.add_cog(On_Guild_Role_Delete(client))