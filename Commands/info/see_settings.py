import discord
from discord.ext import commands
from discord_slash import cog_ext

from sys import path

from discord_slash.context import SlashContext
path.insert(1, "../../Data")
from Data.DB_commands.bot_info import increase_uses
from Data.DB_commands.server_settings import *


class SeeSettings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="see_settings",
        description="See my settings for this server",
        guild_ids=[805867479909924905]
    )
    async def see_settings(self, ctx:SlashContext):
        profanity = get_profanity(ctx)
        w_a_g_c = get_w_a_g_c(ctx).name
        hi_bye_mode = get_hi_bye_mode(ctx)
        mute_role = get_mute_role(ctx)
        
        embed = discord.Embed(
            title="Settings :gear:",
            color=discord.Color.from_rgb(14, 39, 46)
        ).set_author(
            name=ctx.author,
            icon_url=ctx.author.avatar_url
        ).set_thumbnail(
                url=self.client.user.avatar_url
        ).set_footer(
            text="Tip: If you want to change settings, use /setup"
        )

        embed.add_field(name="Welcome and Goodbye Messages", value="```{}```".format("On" if hi_bye_mode == True else "Off"), inline=False)
        embed.add_field(name="Welcome and Goodbye Channel", value=f"```{w_a_g_c}```", inline=False)
        embed.add_field(name="Anti-Profanity Mode", value="```{}```".format("On" if profanity == True else "Off"), inline=False)
        embed.add_field(name="Mute Role", value="{}".format(mute_role.mention if mute_role != None else "```None```"), inline=False)

        await ctx.reply(embed=embed)
        return increase_uses()


def setup(client):
    client.add_cog(SeeSettings(client))