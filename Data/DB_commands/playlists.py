import pymongo

from sys import path

from pymongo.message import _delete_uncompressed
path.insert(1, "../")
from databases import *

def get_playlists(ctx):
    if not if_user_is_found(ctx):
        add_user_to_DB(ctx)

    if(result := youtube_users.find_one({"_id" : ctx.author.id})):
        return result["playlists"]

def get_playlists_num(ctx):
    if not if_user_is_found(ctx):
        add_user_to_DB(ctx)

    if(result := youtube_users.find_one({"_id" : ctx.author.id})):
        return result["pls_size"]

def if_user_is_found(ctx):
    if youtube_users.find_one({"_id" : ctx.author.id}):
        return True
    
    return False

def add_user_to_DB(ctx):
    guild_post = {"_id" : ctx.author.id, "playlists" : dict(), "pls_size" : 0}
    youtube_users.insert_one(guild_post)

def create_playlist(ctx, name : str):
    # if user is not in the DB => he will be added
    if not if_user_is_found(ctx):
        add_user_to_DB(ctx)
    
    # get user's playlists like a dict where key is playlist's name and the value is a tuple with songs
    playlists = get_playlists(ctx)

    if name not in playlists:
        playlists[name] = list()
        youtube_users.update_one({"_id" : ctx.author.id}, {"$set" : {"playlists" : playlists}})
        youtube_users.update_one({"_id" : ctx.author.id}, {"$inc" : {"pls_size" : 1}})
        return True

    else:
        # can't be added
        return False


def remove_playlist(ctx, name : str):
    # if user is not in the DB => he will be added
    if not if_user_is_found(ctx):
        add_user_to_DB(ctx)
        return False

    playlists = get_playlists(ctx)
    
    if playlists == {} or name not in playlists:
        return False

    del playlists[name]

    youtube_users.update_one({"_id" : ctx.author.id}, {"$set" : {"playlists" : playlists}})
    youtube_users.update_one({"_id" : ctx.author.id}, {"$inc" : {"pls_size" : -1}})
    return True

def remove_all(ctx):
    # if user is not in the DB => he will be added
    if not if_user_is_found(ctx):
        add_user_to_DB(ctx)
        return False

    playlists = get_playlists(ctx)
    
    if playlists == {}:
        return False

    youtube_users.update_one({"_id" : ctx.author.id}, {"$set" : {"playlists" : dict()}})
    youtube_users.update_one({"_id" : ctx.author.id}, {"$set" : {"pls_size" : 0}})
    return True

def rename_playlist(ctx, old_name : str, new_name : str):
    # if user is not in the DB => he will be added
    if not if_user_is_found(ctx):
        add_user_to_DB(ctx)
        return False

    playlists = get_playlists(ctx)
    
    if playlists == {}:
        return False
    
    if (old_name in playlists) and (old_name != new_name):
        playlists[new_name] = playlists[old_name]
        del playlists[old_name]

        youtube_users.update_one({"_id" : ctx.author.id}, {"$set" : {"playlists" : playlists}})
        return True
    else:
        return False

def add_song_to_playlist(ctx, playlist, song):
    # if user is not in the DB => he will be added
    if not if_user_is_found(ctx):
        add_user_to_DB(ctx)

    playlists = get_playlists(ctx)
    
    if playlists == {} or playlist not in playlists:
        create_playlist(ctx, playlist)
        playlists = get_playlists(ctx)
    
    playlists[playlist].append(song)

    youtube_users.update_one({"_id" : ctx.author.id}, {"$set" : {"playlists" : playlists}})

def remove_song_from_playlist(ctx, playlist, index : int):
    # if user is not in the DB => he will be added
    if not if_user_is_found(ctx):
        add_user_to_DB(ctx)
        return [False, None, "Not in DB"]

    playlists = get_playlists(ctx)
    
    if playlists == {} or playlist not in playlists:
        return [False, None, "No playlist found"]
    else:
        #           last index
        if (len(playlists[playlist]) - 1) >= index >= 0:
            song = playlists[playlist].pop(index)
            youtube_users.update_one({"_id" : ctx.author.id}, {"$set" : {"playlists" : playlists}})
            return [True, song]
        else:
            return [False, None]