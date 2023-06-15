import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option

from sys import path
path.insert(1, "../../Data")
from Data.DB_commands.bot_info import increase_uses


class EmojiInfo(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_slash(
        name="emoji_info",
        description="Pass in one server emoji and receive its information",
        guild_ids=[805867479909924905]
    )
    async def emoji_info(self, ctx:SlashContext, emoji:discord.Emoji):
        try:
            # gives info about the person that created the emoji
            emoji_info = emoji.split(":")
            # Example: <:cow:875767646124122122> => ['<', 'cow', '875767646124122122>']
            emoji = await ctx.guild.fetch_emoji(int(emoji_info[2].replace('>', '')))
        except:
            error = discord.Embed(title="Error :red_circle:", description="```The emoji must be from this server.```", color=discord.Color.red())
            return await ctx.reply(embed=error)
        
        embed = discord.Embed(title="Emoji Info", color=discord.Color.from_rgb(14, 39, 46))
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=emoji.url)

        embed.add_field(name="Name", value="```{}```".format(emoji.name), inline=True)
        embed.add_field(name="Author", value="```{}```".format(emoji.user), inline=True)
        embed.add_field(name="URL", value="[Link]({})".format(emoji.url), inline=True)

        embed.add_field(name="Is Animated?", value="```{}```".format("Yes" if emoji.animated else "No"), inline=True)
        embed.add_field(name="Is Managed?", value="```{}```".format("Yes" if emoji.managed else "No"), inline=True)
        embed.add_field(name="Requires Colons?", value="```{}```".format("Yes" if emoji.require_colons else "No"), inline=True)
        
        embed.add_field(name="Created At", value="```{}```".format(emoji.created_at.strftime("%a, %#d %B %Y, %I:%M %p, UTC")), inline=True)
        embed.add_field(name="ID", value="```{}```".format(emoji.id), inline=True)
        embed.add_field(name="Usable By", value="{}".format("```Everyone```" if not emoji.roles else " **;**".join(f"```{role.name}```" for role in emoji.roles)), inline=True)

        await ctx.reply(embed=embed)
        return increase_uses()


def setup(client):
    client.add_cog(EmojiInfo(client))