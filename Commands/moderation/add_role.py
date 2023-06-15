import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option

import datetime

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Error.permissions import permission_error
from Error.nwc import nwc
from Error.sww import sww


class AddRole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="add_role",
        description="Adds a specific server role to a member",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="member",
                description="Provide a member",
                required=True,
                option_type=6
            ),
            create_option(
                name="role",
                description="Provide a role",
                required=True,
                option_type=8
            )
        ]
    )
    async def add_role(self, ctx:SlashContext, member:discord.Member, role:discord.Role):
        if not (ctx.author.guild_permissions.manage_guild):
            return await permission_error(self.client, ctx, ["manage_guild"])
        
        if member.id == self.client.user.id:
            return await nwc(ctx, f"```I can't give myself a role!```")
        
        if member.id == ctx.author.id:
            return await nwc(ctx, f"```You can't give yourself a role!```")

        try:
            if role.is_bot_managed():
                if member.id == ctx.author.id:
                    return await nwc(ctx, f"```You can't get a bot-related role!```")
                else:
                    return await nwc(ctx, f"```{member} can't get a bot-related role!```")

            if role in member.roles:
                if member.id == ctx.author.id:
                    return await nwc(ctx, f"```You have this role already!```")
                else:
                    return await nwc(ctx, f"```{member} has this role already!```")

            await member.add_roles(role)
            
            time = datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M %p, UTC")
            
            server_embed = discord.Embed(
                title="New Role Added :white_check_mark:",
                color=discord.Color.from_rgb(14, 39, 46)
            ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url
            ).add_field(name="Member", value=f"{member.mention}", inline=True
            ).set_thumbnail(url=member.avatar_url
            ).add_field(name="New Role", value=f"{role.mention}", inline=True
            ).add_field(name="Added At", value=f"```{time}```", inline=False)

            await ctx.reply(embed=server_embed)
            
            if not member.bot:
                member_embed = discord.Embed(
                    title="New Role Added :white_check_mark:",
                    color=discord.Color.from_rgb(14, 39, 46)
                ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url
                ).set_thumbnail(url=ctx.guild.icon_url
                ).add_field(name="New Role", value=f"```{role.name}```", inline=False
                ).add_field(name="Added At", value=f"```{time}```", inline=False
                ).add_field(name="Server", value=f"```{ctx.guild.name}```", inline=True)

                await member.send(embed=member_embed)

            return increase_uses()

        except:
            client_member = ctx.guild.get_member(user_id=self.client.user.id) # gets client's top role
            sy = ">=" if member.top_role >= client_member.top_role else "<="
            return await sww(ctx, "```I don't have manage_roles permission```{} **OR** ```I don't have permission to give this role```**Role:** {}".format(f"**OR** ```{member.name}'s top role in this server is higher or equal to mine```{member.top_role.mention} **{sy}** {client_member.top_role.mention}\n" if member.id != self.client.user.id else "", role.mention))
            

def setup(client):
    client.add_cog(AddRole(client))