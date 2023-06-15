import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from discord_slash.context import SlashContext

import datetime

from sys import path
path.insert(1, "../../Data")
path.insert(1, "../../Error")

from Data.DB_commands.bot_info import increase_uses
from Error.permissions import *


class UnBan(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="unban",
        description="Given member of this server is unbanned from it",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="user",
                description="Provide a member in this way: <username>#<discriminator>",
                required=True,
                option_type=3
            ),
            create_option(
                name="reason",
                description="What's the reason for unbanning this user?",
                required=False,
                option_type=3
            )
        ]
    )
    async def unban(self, ctx:SlashContext, user:str, reason:str=None):
        if not (ctx.author.guild_permissions.manage_roles and ctx.author.guild_permissions.ban_members):
            return await permission_error(self.client, ctx, permissions=["manage_roles", "ban_members"])

        try:
            # User's name and discriminator
            user_name, user_discriminator = user.split('#')
            banned_users = await ctx.guild.bans()
            found = False
            found_user = None

            # Check for this user in baned users
            for ban_entry in banned_users:
                _user = ban_entry.user
                if (_user.name, _user.discriminator) == (user_name, user_discriminator):
                    found = True
                    reason = "None" if reason == None else reason[:512]
                    await ctx.guild.unban(_user, reason=reason)
                    found_user = _user
                    break
            
            embed = discord.Embed(
                title = "{}".format("Unban :hook:" if found else "No One Was Unbanned!"),
                color = discord.Color.from_rgb(14, 39, 46)
            ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

            if found == True:
                embed.add_field(
                    name="User",
                    value=f"```{found_user.name}```",
                    inline=False
                ).add_field(
                    name="Unbanned At",
                    value="```{}```".format(datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M %p, UTC")),
                    inline=False
                ).add_field(
                    name="Reason",
                    value="```{}```".format(reason),
                    inline=False
                ).set_thumbnail(url=found_user.avatar_url)
                
                await ctx.reply(embed=embed)

                if not found_user.bot:
                    await found_user.send(embed=embed.add_field(name="Server", value=f"```{ctx.guild.name}```").set_thumbnail(url=ctx.guild.icon_url))
                
                return increase_uses()

            else:
                embed.description = "```{} was not found in your server bans!```\n**Possible reasons:**\n:small_blue_diamond: This user was not banned at all.\n:small_blue_diamond: Wrongly written user.".format(user if len(user) <= 37 else user[:34] + "...")
                return await ctx.reply(embed=embed)

        except:
            error = discord.Embed(
                title="No One Was Banned!", #Something Went Wrong!
                description=f"```I don't have ban_members permission``` **OR** ```You didn't follow the syntax: <username>#<discriminator>```",
                color=discord.Color.from_rgb(14, 39, 46)
            ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url).set_footer(text="Tip: You don't have to write < and >")
            return await ctx.reply(embed=error)


def setup(client):
    client.add_cog(UnBan(client))