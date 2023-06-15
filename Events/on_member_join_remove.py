import discord
from discord.ext import commands

import datetime

from sys import path
path.insert(1, "../Data")
from Data.DB_commands.server_settings import *


class On_Member_Join_Remove(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def is_banned(self, member):
        try:
            found = False
            banned_users = await member.guild.bans()
            for ban_entry in banned_users:
                _user = ban_entry.user
                if _user == member:
                    found = True
                    break
            
            return found

        except:
            return False
    
    async def is_kicked(self, member):
        try:
            async for entry in member.guild.audit_logs(limit=100):
                if entry.action == discord.AuditLogAction.kick and entry.target.id == member.id:
                    return True, entry.user # who did it
                
            return False, None

        except:
            return False, None


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if get_hi_bye_mode(member) == True:
            channel = get_w_a_g_c(member)

            if channel == None:
                channel = await member.guild.create_text_channel("welcome-and-goodbye")
                await channel.set_permissions(channel.guild.default_role, send_messages=False)
                update_w_a_g_c(member, channel)
                
            hello = discord.Embed(title="Member Joined :heavy_plus_sign:", color=discord.Color.dark_green())
            hello.set_author(name=member, icon_url=member.avatar_url)
            hello.set_thumbnail(url=member.avatar_url)

            hello.add_field(name=f"Joined At", value="```{}```".format(datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M %p, UTC")), inline=False)
            hello.add_field(name=f"Member Count", value="```{}```".format(member.guild.member_count), inline=False)
            
            return await channel.send(embed=hello)
        else:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if get_hi_bye_mode(member) == True:
            channel = get_w_a_g_c(member)

            if channel == None:
                channel = await member.guild.create_text_channel("welcome-and-goodbye")
                await channel.set_permissions(channel.guild.default_role, send_messages=False)
                update_w_a_g_c(member, channel)

            if await self.is_banned(member):
                return

            is_kicked, kicker = await self.is_kicked(member)

            bye = discord.Embed(title="Member {}".format("Kicked :gloves:" if is_kicked else "Left :heavy_minus_sign:"), color=discord.Color.dark_magenta())
            bye.set_author(name=kicker if is_kicked else member, icon_url=member.avatar_url if is_kicked == False else kicker.avatar_url)
            bye.set_thumbnail(url=member.avatar_url)

            bye.add_field(name="{} At".format("Kicked" if is_kicked else "Left"), value="```{}```".format(datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M %p, UTC")), inline=False)
            bye.add_field(name=f"Member Count", value="```{}```".format(channel.guild.member_count), inline=False)
            
            return await channel.send(embed=bye)


# Connects this functionality to the bot
def setup(client):
    client.add_cog(On_Member_Join_Remove(client))