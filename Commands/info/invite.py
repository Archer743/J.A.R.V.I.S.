import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.context import SlashContext

from sys import path
path.insert(1, "../../Data")
from Data.DB_commands.bot_info import increase_uses

import json
with open('./Data/config.json') as file:
    data = json.load(file)


class Invite(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_slash(
        name="invite",
        description="Provides my invite links",
        guild_ids=[805867479909924905]
    )
    async def invite(self, ctx:SlashContext):
        embed = discord.Embed(name="Invite Links", color=discord.Color.from_rgb(14, 39, 46))
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=self.client.user.avatar_url)

        embed.description = f"""
        :small_blue_diamond: [Without Permissions]({data["without_permissions_invite_link"]})
        :small_blue_diamond: [Administrator Permissions]({data["admin_permissions_invite_link"]})
        :small_blue_diamond: [All Needed Permissions]({data["all_needed_permissions_invite_link"]})
        """
        

        await ctx.reply(embed=embed)
        return increase_uses()


def setup(client):
    client.add_cog(Invite(client))