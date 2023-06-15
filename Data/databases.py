import pymongo
from pymongo import MongoClient
import json


with open("./Data/config.json", "r") as file:
    data = json.load(file)

cluster = MongoClient(data["DB"]["URI"], connect=False)

# DBs
db_servers = cluster["servers"]
db_youtube = cluster["youtube"]
db_bot = cluster["bot"]

# Collections
prefix_collection = db_servers["prefix"]

subscribers_collection = db_youtube["subscribers"]
youtube_users = db_youtube["users"]

bot_info = db_bot["info"]