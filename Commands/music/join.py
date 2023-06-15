import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.context import SlashContext

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")
from Data.DB_commands.bot_info import increase_uses
from Error.music import out_of_vc
from Error.sww import *


class Join(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="join", description="Adds me to your current voice channel", guild_ids=[805867479909924905])
    async def join(self, ctx:SlashContext):
        a_voice_state = ctx.author.voice
        bot_voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if a_voice_state is None:
            return await out_of_vc(ctx, f"```You are not in a voice channel!```")

        if bot_voice != None:
            return await out_of_vc(ctx, f"```I am in a voice channel already!```")

        try:
            vc = ctx.author.voice.channel
            await vc.connect()

            embed = discord.Embed(
                title="Join :headphones:",
                description=f"**Added to** {vc.mention} **by** {ctx.author.mention}!",
                color=discord.Color.from_rgb(14, 39, 46)
            ).set_author(name=self.client.user, icon_url=self.client.user.avatar_url)

            await ctx.reply(embed=embed)
            return increase_uses()

        except:
            return await sww(ctx, "")


def setup(client):
    client.add_cog(Join(client))