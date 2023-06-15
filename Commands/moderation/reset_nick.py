import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from discord_slash.context import SlashContext

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Error.permissions import *
from Error.nwc import nwc


class ResetNick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="reset_nick",
        description="Resets member's nickname in this server",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="member",
                description="Provide a member to whom you will reset the nickname",
                required=True,
                option_type=6
            )
        ]
    )
    async def reset_nick(self, ctx:SlashContext, member:discord.Member):
        if not (ctx.author.guild_permissions.change_nickname and ctx.author.guild_permissions.manage_nicknames):
            return await permission_error(self.client, ctx, permissions=["change_nickname", "manage_nicknames"])
        
        try:
            if member.nick == None:
                return await nwc(ctx, f"```{member} already has a default nickname!```")
            
            await member.edit(nick=None)

            embed=discord.Embed(
                title="Nick Reset :pencil:",
                color=discord.Color.from_rgb(14, 39, 46)
            ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url
            ).add_field(name="Member", value=f"```{member}```", inline=True
            ).add_field(name="New Nick", value=f"```{member.nick}```")

            await ctx.reply(embed=embed)

            if not member.bot:
                await member.send(embed=embed.set_thumbnail(url=ctx.guild.icon_url).add_field(name="Server", value=f"```{ctx.guild}```"))
            
            return increase_uses()

        except:
            client_member = ctx.guild.get_member(user_id=self.client.user.id) # gets client's top role
            sy = ">=" if member.top_role >= client_member.top_role else "<="
            return await nwc(ctx, f"```{member.name}'s top role in the server is higher or equal to mine!```{member.top_role.mention} **{sy}** {client_member.top_role.mention}")


def setup(client):
    client.add_cog(ResetNick(client))        