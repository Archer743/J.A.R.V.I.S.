# w_a_g_c => welcome and goodbye channel => when member joins or leaves
# provides info about hi_and_bye_mode and provides channel 
# in which embeds will be send if member joins or leaves

import discord
import pymongo

from sys import path
path.insert(1, "../")
from databases import *


# returns if there will be any messages on join_left event for members
def get_hi_bye_mode(member):
    if (result := prefix_collection.find_one({"_id" : member.guild.id})):
        return result["hi_and_bye_mode"]
    else:
        return None

def get_hi_bye_mode_from_guild(guild):
    if (result := prefix_collection.find_one({"_id" : guild.id})):
        return result["hi_and_bye_mode"]
    else:
        return None

# updates this mode of receiving messages on join_left event for members
def update_hi_bye_mode(member, mode:bool):
    prefix_collection.update_one({"_id" : member.guild.id}, {"$set" : {"hi_and_bye_mode" : mode}})


# returns the channel in which there will be sent messages on join_left event for members
def get_w_a_g_c(member):
    if (result := prefix_collection.find_one({"_id" : member.guild.id})):
        return discord.utils.get(member.guild.channels, id=result["w_a_g_c"])
    else:
        return None

def get_w_a_g_c_from_guild(guild):
    if (result := prefix_collection.find_one({"_id" : guild.id})):
        return discord.utils.get(guild.channels, id=result["w_a_g_c"])
    else:
        return None

# updates the channel in which there will be sent messages on join_left event for members
def update_w_a_g_c(member, channel):
    prefix_collection.update_one({"_id" : member.guild.id}, {"$set" : {"w_a_g_c" : channel.id}})


# returns the anti-profanity mode -> if it is on or off (bool)
def get_profanity(ctx):
    if (result := prefix_collection.find_one({"_id" : ctx.guild.id})):
        return result["profanity"]

# updates the anti-profanity mode
def update_profanity(ctx, mode:bool):
    prefix_collection.update_one({"_id" : ctx.guild.id}, {"$set" : {"profanity" : mode}})


# returns the server's mute role
def get_mute_role(ctx):
    if (result := prefix_collection.find_one({"_id" : ctx.guild.id})):
        # if mute role found -> returns object with discord.Role type else -> returns None(mute role not found)
        return discord.utils.get(ctx.guild.roles, id=result["mute_role"])

# returns the server's mute role id
def get_mute_role_id(ctx):
    if (result := prefix_collection.find_one({"_id" : ctx.guild.id})):
        # if mute role found -> returns object with discord.Role type else -> returns None(mute role not found)
        return result["mute_role"]
        
# updates the mute role
def update_mute_role(ctx, new_role:discord.Role=None):
    if not new_role:
        prefix_collection.update_one({"_id" : ctx.guild.id}, {"$set" : {"mute_role" : None}})
    else:
        prefix_collection.update_one({"_id" : ctx.guild.id}, {"$set" : {"mute_role" : new_role.id}})