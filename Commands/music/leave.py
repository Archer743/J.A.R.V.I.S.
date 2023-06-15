import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")
from Data.DB_commands.bot_info import increase_uses
from Error.sww import *
from Error.music import out_of_vc


class Leave(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="leave", description="Disconnects me from my current voice channel", guild_ids=[805867479909924905])
    async def leave(self, ctx:SlashContext):
        try:
            if ctx.author.voice is None:
                return await out_of_vc(ctx, f"```You are not in a voice channel!```")
            
            if ctx.voice_client is None:
                return await out_of_vc(ctx, f"```I am not in a voice channel!```")

            if ctx.author.voice.channel == ctx.voice_client.channel:
                vc = ctx.voice_client.channel
                await ctx.voice_client.disconnect(force=True)
                
                embed = discord.Embed(
                    title="Leave :airplane_departure:",
                    description=f"**Removed from** {vc.mention} **by** {ctx.author.mention}!",
                    color=discord.Color.from_rgb(14, 39, 46)
                ).set_author(name=self.client.user, icon_url=self.client.user.avatar_url)
                
                await ctx.reply(embed=embed)
                return increase_uses()

            else:
                return await out_of_vc(ctx, f"```We have to be connected to the same voice channel so you can disconnect me!```")
        
        except:
            return await sww(ctx, "")


def setup(client):
    client.add_cog(Leave(client))