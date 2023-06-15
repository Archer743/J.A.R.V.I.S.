import discord
from discord.ext import commands

from discord_slash import cog_ext

import datetime

from sys import path
path.insert(1, "../../Data")
from Data.DB_commands.server_settings import *


class On_Member_Unban(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def find_unbanner(self, guild:discord.Guild, user:discord.User):
        try:
            async for entry in guild.audit_logs(limit=100):
                if entry.action == discord.AuditLogAction.unban and entry.target.id == user.id:
                    return entry.user # who did it
            
            return None

        except:
            return None

    @commands.Cog.listener()
    async def on_member_unban(self, guild:discord.Guild, user:discord.User):
        if get_hi_bye_mode_from_guild(guild) == True:
            channel = get_w_a_g_c_from_guild(guild)

            if channel == None:
                channel = await user.guild.create_text_channel("welcome-and-goodbye")
                await channel.set_permissions(channel.guild.default_role, send_messages=False)
                update_w_a_g_c(user, channel)

            unbanner = await self.find_unbanner(guild, user)

            unban = discord.Embed(title="Member Unbanned :hook:", color=discord.Color.dark_green())
            unban.set_author(name=unbanner if unbanner != None else user, icon_url=unbanner.avatar_url if unbanner != None else user.avatar_url)

            unban.set_thumbnail(url=user.avatar_url)
            
            unban.add_field(name=f"Unbanned At", value="```{}```".format(datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M %p, UTC")), inline=False)
            unban.add_field(name=f"Member Count", value="```{}```".format(guild.member_count), inline=False)
            
            return await channel.send(embed=unban)


def setup(client):
    client.add_cog(On_Member_Unban(client))