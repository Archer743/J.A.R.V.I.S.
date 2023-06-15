import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option

from sys import path
path.insert(1, "../../Data")
from Data.DB_commands.bot_info import increase_uses

from reactionmenu import ReactionMenu


class RoleInfo(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_slash(
        name="role_info",
        description="Provides information about a role",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="role",
                description="Provide a role",
                required=True,
                option_type=8
            )
        ]
    )
    async def role_info(self, ctx:SlashContext, role):
        menu = ReactionMenu(ctx, back_button="⬅️", next_button="➡️", config=ReactionMenu.STATIC, timeout=120.0)

        first_page = discord.Embed(title="Role Info", color=role.color)
        first_page.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        first_page.add_field(name="Name", value=f"{role.mention}", inline=True)
        first_page.add_field(name="ID", value=f"```{role.id}```", inline=True)
        first_page.add_field(name="Position", value=f"```{role.position}```", inline=True)

        first_page.add_field(name="Is Default?", value="```{}```".format("Yes" if role.is_default() == True else "No"), inline=True)
        first_page.add_field(name="Is Mentionable?", value="```{}```".format("Yes" if role.mentionable == True else "No"), inline=True)
        first_page.add_field(name="Is Separated?", value="```{}```".format("Yes" if role.hoist == True else "No"), inline=True)
        first_page.add_field(name="Is Bot Related?", value="```{}```".format("Yes" if role.is_bot_managed() == True else "No"), inline=True)
        first_page.add_field(name="Boost Role?", value="```{}```".format("Yes" if role.is_premium_subscriber() == True else "No"), inline=True)

        first_page.add_field(name='Created At', value=f'```{role.created_at.strftime("%a, %#d %B %Y, %I:%M %p, UTC")}```', inline=True)
        first_page.add_field(name='Members', value='```{}```'.format(number if (number := len(role.members)) != 0 else "None"), inline=True)
        

        second_page = discord.Embed(title="Permissions", color=role.color)
        second_page.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        
        # =================================================
        permissions = [list(permission) for permission in role.permissions]
        true_permissions = []
        for permission in permissions:
            if permission[1] == True:
                true_permissions.append(permission[0])
        
        if true_permissions != []:
            second_page.description = "**;** ".join([f"``{str(permission)}``" for permission in true_permissions])
        else:
            second_page.description = "```None```"
        # =================================================
        
        menu.add_page(first_page)
        menu.add_page(second_page)
        await menu.start()
        return increase_uses()


def setup(client):
    client.add_cog(RoleInfo(client))