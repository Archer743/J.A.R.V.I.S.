import discord
from discord.ext import commands

from discord_slash import cog_ext

from sys import path
from discord_slash.context import SlashContext

from discord_slash.utils.manage_commands import create_option
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Error.permissions import *
from Error.nwc import nwc


class Nick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="nick",
        description="Changes member's nick in this server",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="member",
                description="Provide a member to whom you will change the nickname",
                required=True,
                option_type=6
            ),
            create_option(
                name="nick",
                description="Provide nickname",
                required=True,
                option_type=3
            )
        ]
    )
    async def nick(self, ctx:SlashContext, member:discord.Member, nick:str):
        if not ctx.author.guild_permissions.manage_nicknames:
            return await permission_error(self.client, ctx, ["manage nicknames"])
        
        try:
            if nick == member.nick or nick == member.name:
                return await nwc(ctx, f"```{member} already has that nickname!```")

            elif len(nick) > 32:
                return await nwc(ctx, f"```Nickname length must be less than ***32***```")
            
            await member.edit(nick=nick)

            embed=discord.Embed(
                title="New Nick :pencil:",
                color=discord.Color.from_rgb(14, 39, 46)
            ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url
            ).add_field(name="Member", value=f"```{member}```", inline=True
            ).add_field(name="New Nick", value=f"```{nick}```")

            await ctx.reply(embed=embed)

            if not member.bot:
                await member.send(embed=embed.set_thumbnail(url=ctx.guild.icon_url).add_field(name="Server", value=f"```{ctx.guild}```"))
            return increase_uses()
        
        except:
            client_member = ctx.guild.get_member(user_id=self.client.user.id) # gets client's top role
            sy = ">=" if member.top_role >= client_member.top_role else "<="
            return await nwc(ctx, f"```{member.name}'s top role in the server is higher or equal to mine!```{member.top_role.mention} **{sy}** {client_member.top_role.mention}")


def setup(client):
    client.add_cog(Nick(client))