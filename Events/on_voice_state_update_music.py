import discord
from discord.ext import commands


class On_Voice_State_Update(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    # Bot leaves voice channel when he is the last one in it!
    async def on_voice_state_update(self, member, before, after):  
        try:
            #                                        real people in a voice channel
            if self.client.user in before.channel.members and len([m for m in before.channel.members if not m.bot]) == 0:
                channel = discord.utils.get(self.client.voice_clients, channel=before.channel)
                await channel.disconnect()
        except:
            pass


# Connects this functionality to the bot
def setup(client):
    client.add_cog(On_Voice_State_Update(client))