import pymongo

from sys import path
path.insert(1, "../")
from databases import *

# returns how many slash commands does the bot has
# command for updating that number is in on_start.py -> update_commands_number()
def get_commands_number():
    if (result := bot_info.find_one({"_id" : 1})):
        return result["commands"]

# return how many times does the bot was used
def get_uses():
    if (result := bot_info.find_one({"_id" : 0})):
        return result["all_uses"]

# returns the bot's start time
def get_start_time():
    if (result := bot_info.find_one({"_id" : 2})):
        return result["time_float"], result["time_text"]

# updates the number of uses of the bot
def increase_uses():
    bot_info.update_one({"_id" : 0}, {"$inc" : {"all_uses" : 1}})