import discord
from discord.ext import commands
from discord_slash import cog_ext

from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Data.DB_commands.server_settings import get_profanity, update_profanity

from Error.permissions import *


class Profanity(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="profanity",
        description="See or change my anti-profanity mode for this server",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="option",
                description="Choose option",
                required=True,
                option_type=3,
                choices=[
                    create_choice(name="See", value="see"),
                    create_choice(name="Edit", value="edit")
                ]
            ),
            create_option(
                name="toggle",
                description="Choose my anti-profanity mode in this server",
                required=False,
                option_type=5
            )
        ]
    )
    async def profanity(self, ctx:SlashContext, option:str, toggle:bool = None):
        if option == "see" or toggle == None:
            embed = discord.Embed(description="```Anti-Profanity Mode is {}!```".format("On" if get_profanity(ctx) == True else "Off"), color=discord.Color.from_rgb(14, 39, 46))
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            
            await ctx.reply(embed = embed)
            return increase_uses()

        else:
            if not (ctx.author.guild_permissions.manage_guild and ctx.author.guild_permissions.manage_messages):
                return await permission_error(self.client, ctx, ["manage guild", "manage messages"])

            # Boolean
            profanity_mode = get_profanity(ctx)
        
            if profanity_mode != toggle:
                update_profanity(ctx, mode=toggle)
                embed = discord.Embed(description="```Anti-Profanity Mode {}!```".format("On" if toggle == True else "Off"), color=discord.Color.from_rgb(14, 39, 46))
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.reply(embed = embed)

            else:
                embed = discord.Embed(description="```Anti-Profanity Mode Is Already {}!```".format("On" if toggle == True else "Off"), color=discord.Color.from_rgb(14, 39, 46))
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.reply(embed = embed)

            return increase_uses()


def setup(client):
    client.add_cog(Profanity(client))