import pymongo

# Time
import time
import datetime

from sys import path
path.insert(1, "../")
from databases import *

# Updates Start Time
def update_start_time():
    bot_info.update_one({"_id" : 2}, {"$set" : {"time_float" : time.time(), "time_text" : datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M %p, UTC")}})

# Updates the number of bot's slash commands
def update_commands_number(number_of_commands):
    bot_info.update_one({"_id" : 1}, {"$set" : {"commands" : number_of_commands}})