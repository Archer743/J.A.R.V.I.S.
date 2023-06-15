import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.context import SlashContext

import requests, json

from sys import path
path.insert(1, "../../Data")
from Data.DB_commands.bot_info import increase_uses


class Inspire(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    def get_quote_and_author(self):
        response = requests.get("https://zenquotes.io/api/random") # link for quotes
        json_data = json.loads(response.text)
        return json_data[0]['q'], json_data[0]['a']

    @cog_ext.cog_slash(name="inspire", description="Gives you a wise thought of a famous person", guild_ids=[805867479909924905])
    async def inspire(self, ctx:SlashContext):
        quote, author = self.get_quote_and_author()

        embed = discord.Embed(
            title="QUOTE",
            description=f'''***```"{quote}"```***''',
            color=discord.Color.from_rgb(14, 39, 46)
        ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url
        ).set_footer(text=f"By {author}")

        await ctx.reply(embed=embed)
        return increase_uses()

    
def setup(client):
    client.add_cog(Inspire(client))