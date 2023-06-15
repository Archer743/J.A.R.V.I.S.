import discord
from discord.ext import commands


class On_Disconnect(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_disconnect(self, ctx):
        print("Disconnected!")
        await ctx.send("Disconnected!")


# Connects this functionality to the bot
def setup(client):
    client.add_cog(On_Disconnect(client))