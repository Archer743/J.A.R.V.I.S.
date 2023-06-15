import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Data.DB_commands.server_settings import *

from Error.permissions import *


class Set_Up(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="setup",
        description="Sets everything that will be needed in my future work",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="w_a_g_m",
                description="Do you want to receive message when someone joins or leaves you server?",
                required=False,
                option_type=5
            ),
            create_option(
                name="w_a_g_c",
                description="Provide a text channel in which you will receive welcome and goodbye messages",
                required=False,
                option_type=7
            ),
            create_option(
                name="profanity",
                description="Do you want to activate anti-profanity mode?",
                required=False,
                option_type=5
            ),
            create_option(
                name="mute_role",
                description="Do you want to change the server's mute role?",
                required=False,
                option_type=8
            )
        ]   
    )
    async def set_up(self, ctx:SlashContext, w_a_g_m:bool = None, w_a_g_c = None, profanity:bool = None, mute_role:discord.Role = None):      
        if not (ctx.author.guild_permissions.manage_guild and ctx.author.guild_permissions.manage_messages):
            return await permission_error(self.client, ctx, ["manage guild", "manage messages"])

        embed = discord.Embed(color=discord.Color.from_rgb(14, 39, 46))
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        w_a_g_m_changed = False
        w_a_g_c_changed = False
        profanity_changed = False
        mute_role_changed = False

        if w_a_g_m == None and w_a_g_c == None and profanity == None and mute_role == None:
            embed.title="Nothing Was Changed!"
            return await ctx.reply(embed=embed)
        
        if w_a_g_m != None and get_hi_bye_mode(ctx) != w_a_g_m:
            update_hi_bye_mode(ctx, w_a_g_m)
            w_a_g_m_changed = True
            embed.add_field(name="Welcome and Goodbye Messages", value="```{}```".format("On" if w_a_g_m == True else "Off"), inline=False)

        if w_a_g_c != None and get_w_a_g_c(ctx) != w_a_g_c:
            if str(w_a_g_c.type) == "text":
                update_w_a_g_c(ctx, channel=w_a_g_c)
                w_a_g_c_changed = True
                embed.add_field(name="Welcome and Goodbye Channel", value=f"```{w_a_g_c}```", inline=False)
            else:
                embed.add_field(name=":diamonds: Welcome and Goodbye Channel", value=f"```Text channel required. Type provided - {str(w_a_g_c.type)}.```")
        
        if profanity != None and get_profanity(ctx) != profanity:
            update_profanity(ctx, mode=profanity)
            profanity_changed = True
            embed.add_field(name="Anti-Profanity Mode", value="```{}```".format("On" if profanity == True else "Off"), inline=False)

        if mute_role != None and get_mute_role(ctx).id != mute_role.id:
            if not mute_role.is_bot_managed():
                update_mute_role(ctx, new_role=mute_role)
                mute_role_changed = True
                embed.add_field(name="Mute Role", value=f"{mute_role.mention}", inline=False)
            else:
                embed.add_field(name=":diamonds: Mute Role", value=f"```You can't set the server's mute role to a bot-related one.```")


        if w_a_g_m_changed == False and w_a_g_c_changed == False and profanity_changed == False and mute_role_changed == False:
            embed.title="Nothing Was Changed!"
            return await ctx.reply(embed=embed)
        else:
            embed.set_thumbnail(url=ctx.guild.icon_url)
            
            # has fields
            embed.title = "Changes"
            await ctx.reply(embed=embed)
            return increase_uses()


def setup(client):
    client.add_cog(Set_Up(client))