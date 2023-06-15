import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option


from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Error.permissions import *
from Error.nwc import *
from Error.sww import *
from Error.lockdown import *


class Lockdown(commands.Cog):
    def __init__(self, client):
        self.client = client


    @cog_ext.cog_slash(
        name="lockdown",
        description="Locks a given text channel",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="channel",
                description="Provide a text channel",
                required=False,
                option_type=7
            ),
            create_option(
                name="all",
                description="Do you want to lock every channel on this server?",
                required=False,
                option_type=5
            )
        ]
    )
    async def lockdown(self, ctx:SlashContext, channel:discord.TextChannel=None, all:bool=False):
        if not(ctx.author.guild_permissions.manage_channels):
            return await permission_error(ctx, permissions=["manage_channels"])
        
        channel = channel if channel != None else ctx.channel

        if str(channel.type) != "text":
            return await nwc(ctx, f"{channel.mention} is not a text channel!")

        try:
            if all == False:
                if ctx.guild.default_role not in channel.overwrites:
                    overwrites = channel.overwrites[ctx.guild.default_role]
                    overwrites.send_messages = False
                    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)

                    embed = discord.Embed(title="Channel Locked :lock:", description=f"{channel.mention} is now in lockdown!", color=discord.Color.from_rgb(255,215,0))
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=embed)
                
                elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
                    overwrites = channel.overwrites[ctx.guild.default_role]
                    overwrites.send_messages = False
                    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)

                    embed = discord.Embed(title="Channel Locked :lock:", description=f"{channel.mention} is now in lockdown!", color=discord.Color.from_rgb(255,215,0))
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=embed)
                
                else:
                    return await nwc(ctx, f"{channel.mention} is already locked!")

            else:
                embed = discord.Embed(title="{}".format("Channels Locked :lock:" if len(ctx.guild.channels) >= 2 else "Channel Locked :lock:"), description=f"``{len(ctx.guild.channels)}`` **channels will be in lockdown after a while!**", color=discord.Color.from_rgb(255,215,0))
                message = await ctx.reply(embed=embed)
                
                channels_edited = 0
                text_channels = 0

                for channel in ctx.guild.channels:
                    if str(channel.type) == "text":
                        text_channels += 1
                        if ctx.guild.default_role not in channel.overwrites:
                            overwrites = channel.overwrites[ctx.guild.default_role]
                            overwrites.send_messages = False
                            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
                            channels_edited += 1
                        
                        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
                            overwrites = channel.overwrites[ctx.guild.default_role]
                            overwrites.send_messages = False
                            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
                            channels_edited += 1

                        else:
                            pass
                        
                    else:
                        pass
                
                if channels_edited == 0:
                    return await message.edit(embed = nwc_embed(ctx, "```This server is already locked!```"))
                
                if channels_edited != text_channels:
                    return await message.edit(embed = channels_locked(ctx, channels_edited, text_channels))
                else:
                    embed.description = "**Done!** :white_check_mark:"
                    return await message.edit(embed = embed)

            return increase_uses()
        
        except:
            return await sww(ctx, "")


def setup(client):
    client.add_cog(Lockdown(client))