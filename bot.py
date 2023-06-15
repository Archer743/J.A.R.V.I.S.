import discord
# ext = extension
from discord.ext import commands
from discord_slash import SlashCommand

# DB and COMMents(commands and events)
from sys import path
path.insert(1, "./Data")

from Data.Loading.load_commands_and_events import *
from Data.DB_commands.bot_info import get_commands_number
from Data.DB_commands.on_start import *

import json
with open("./Data/config.json", "r") as file:
    data = json.load(file)

# Bot
# To access member's info like name and prisastvie <= intents
client = commands.Bot(command_prefix = "MCu_!s_THe_B_sT_", intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
client.remove_command('help')

@client.event
async def on_ready():
    '''for command in slash.commands:
        print(f"->{command}")'''

    # Updates Start Time
    update_start_time()
    
    if (get_commands_number()) != (number := (len(slash.commands) - 1)):
        update_commands_number(number)


load_commands(client)
client.run(data["token"])