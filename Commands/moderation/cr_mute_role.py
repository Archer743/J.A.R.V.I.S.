import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Data.DB_commands.server_settings import update_mute_role
from Error.permissions import *
from Error.sww import *
from Error.mute import mute_role_created


class CreateMuteRole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="cr_mute_role",
        description="Creates a mute role for your server",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="name",
                description="Role's name",
                required=False,
                option_type=3
            ),
            create_option(
                name="set_as_server_mute_role",
                description="Do you want my /mute command to use this role?",
                required=False,
                option_type=5
            )
        ]
    )
    async def cr_mute_role(self, ctx:SlashContext, name:str=None, set_as_server_mute_role:bool=False):
        if not (ctx.author.guild_permissions.manage_guild):
            return await permission_error(ctx, permissions=["manage_guild"])

        try:
            name = "Muted" if name == None else name
            #color = discord.Color.red() if color == None else self.get_color(color)
            mute_role = await ctx.guild.create_role(name=name, colour=discord.Color.from_rgb(255, 0, 0)) # dark red
            
            await mute_role_created(ctx, mute_role, perms=["speak - False", "send_messages - False", "read_message_history - False", "read_messages - False"])
            
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=False, read_messages=False)

            if set_as_server_mute_role:
                update_mute_role(ctx, mute_role)
            
            return increase_uses()

        except:
            return await sww(ctx, "")


def setup(client):
    client.add_cog(CreateMuteRole(client))