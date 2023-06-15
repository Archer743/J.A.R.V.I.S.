import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option

from sys import path
path.insert(1, "../../Data")
from Data.DB_commands.bot_info import increase_uses


class ChannelInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Has error handling
    @cog_ext.cog_slash(
        name="channel_info",
        description="Provides information about a channel",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="channel",
                description="Provide a channel",
                required=False,
                option_type=7
            )
        ]
    )
    async def channel_info(self, ctx:SlashContext, channel:str = None):
        if channel == None:
            channel = ctx.channel
        
        list_of_bots = [bot.mention for bot in ctx.channel.members if bot.bot]
        invite_link = await ctx.channel.create_invite(max_uses=100,unique=True)

        embed=discord.Embed(title='Channel Info', color=discord.Color.from_rgb(14, 39, 46))

        embed.add_field(name='Name', value=f'```{channel.name}```', inline=True)
        embed.add_field(name='ID', value=f'```{channel.id}```', inline=True)

        try:
            owner = self.client.get_user(int(ctx.guild.owner_id))
            embed.add_field(name='Owner', value=f'```{owner}```', inline=True)
        except:
            pass
        
        embed.add_field(name='Created At', value=f'```{channel.created_at.strftime("%a, %#d %B %Y, %I:%M %p, UTC")}```', inline=True)
        embed.add_field(name="Type", value=f'```{channel.type}```', inline=True)
        
        if not isinstance(channel, discord.CategoryChannel):
            category = discord.utils.get(ctx.guild.categories, id=channel.category_id)
            embed.add_field(name='Category', value="```{}```".format(category.name if category != None else "None"), inline=True)
            
            if str(channel.type) == "text" or str(channel.type) == "stage":
                embed.add_field(name="Topic:", value='```{}```'.format(channel.topic if (channel.topic != None) else "None"), inline=True)
            elif channel.type == discord.ChannelType.voice:
                embed.add_field(name="User Limit", value='```{}```'.format(channel.user_limit if channel.user_limit != 0 else "None"), inline=True)

            embed.add_field(name='Member Count', value=f"```{len(channel.members)}```", inline=True)
        
        
        embed.add_field(name="Invite Link", value=f"[Channel's Intive Link]({invite_link})", inline=True)
        embed.add_field(name=f'Bots ({len(list_of_bots)})', value=', '.join(list_of_bots) if list_of_bots != [] else "```There are no bots in this channel!```", inline=True)

        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        increase_uses()
        return await ctx.reply(embed=embed)
    

def setup(client):
    client.add_cog(ChannelInfo(client))