import discord
from discord.ext import commands

import datetime

from sys import path
path.insert(1, "../Data")
from Data.DB_commands.server_settings import *


class On_Member_Ban(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def find_banner(self, guild:discord.Guild, user:discord.User):
        try:
            async for entry in guild.audit_logs(limit=100):
                if entry.action == discord.AuditLogAction.ban and entry.target.id == user.id:
                    return entry.user # who did it
            
            return None

        except:
            return None

    @commands.Cog.listener()
    async def on_member_ban(self, guild:discord.Guild, user:discord.User):
        if get_hi_bye_mode(user) == True:
            channel = get_w_a_g_c(user)

            if channel == None:
                channel = await user.guild.create_text_channel("welcome-and-goodbye")
                await channel.set_permissions(channel.guild.default_role, send_messages=False)
                update_w_a_g_c(user, channel)

            banner = await self.find_banner(guild, user)

            ban = discord.Embed(title="Member Banned :hammer:", color=discord.Color.dark_magenta())
            ban.set_author(name=banner if banner != None else user, icon_url=banner.avatar_url if banner != None else user.avatar_url)
            ban.set_thumbnail(url=user.avatar_url)
            
            ban.add_field(name=f"Banned At", value="```{}```".format(datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M %p, UTC")), inline=False)
            ban.add_field(name=f"Member Count", value="```{}```".format(guild.member_count), inline=False)
            ban.add_field(name=f"For Future Unban", value=f"{user.mention}", inline=False)
            
            return await channel.send(embed=ban)


# Connects this functionality to the bot
def setup(client):
    client.add_cog(On_Member_Ban(client))