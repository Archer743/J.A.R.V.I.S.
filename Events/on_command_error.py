import discord
from discord.ext import commands


class On_Command_Error(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    ''''''
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed()
            embed.title="Error :red_circle: "
            embed.description=f"You don't have the permission to use this command."
            embed.color=discord.Color.red()

            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed()
            embed.title="Error :red_circle: "
            embed.description=f"Please pass in all required arguments."
            embed.color=discord.Color.red()

            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed()            
            embed.title="Error :red_circle: "
            embed.description=f'Not a valid argument!\n{error}'
            embed.color=discord.Color.red()

            await ctx.send(embed=embed)
        else:
            print(error)

        '''else:
            embed = discord.Embed(title='Unknown error :red_circle: ', description=f'{error}', color=discord.Color.red())'''
        
        '''if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title="Error :red_circle: ", description=f"Invalid command is used.", color=discord.Color.red())
        else:
            embed = discord.Embed(title='Unknown error :red_circle: ', description=f'{error}', color=discord.Color.red())'''
    

# Connects this functionality to the bot
def setup(client):
    client.add_cog(On_Command_Error(client))