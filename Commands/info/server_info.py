import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option

from sys import path
path.insert(1, "../../Data")
from Data.DB_commands.bot_info import increase_uses


class ServerInfo(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_slash(name="server_info", description="Provides information about this server", guild_ids=[805867479909924905])
    async def server_info(self, ctx:SlashContext):
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
        owner = self.client.get_user(int(ctx.guild.owner_id))

        channels = len(ctx.guild.channels)
        text_channels = 0
        voice_channels = 0
        categories = 0

        for channel in ctx.guild.channels:
            if str(channel.type) == "text":
                text_channels += 1
            elif str(channel.type) == "voice":
                voice_channels += 1
            elif str(channel.type) == "category":
                categories += 1

        embed = discord.Embed(title='Server Info', colour=discord.Color.from_rgb(14, 39, 46))

        embed.add_field(name='Name', value=f'```{ctx.guild.name}```', inline=True)
        embed.add_field(name='ID', value=f'```{ctx.guild.id}```', inline=True)
        embed.add_field(name='Owner', value=f'```{owner}```', inline=True)
        
        embed.add_field(name='Created At', value=f'```{ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p, UTC")}```', inline=True)
        embed.add_field(name='Verification Level', value=f"```{str(ctx.guild.verification_level)}```", inline=True)
        embed.add_field(name='Member Count', value=f"```{ctx.guild.member_count}```", inline=True)
        
        embed.add_field(name=f"Channels ({channels})", value=f"```Text: {text_channels}   Voice: {voice_channels}   Categories: {categories}```")
        embed.add_field(name='Number of Roles', value=f'```{role_count}```', inline=True)
        embed.add_field(name=f'Highest Role', value=f'{ctx.guild.roles[-1].mention}', inline=True)
        
        embed.add_field(name=f'Bots ({len(list_of_bots)})', value=', '.join(list_of_bots), inline=True)
        
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        
        increase_uses()
        return await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(ServerInfo(client))