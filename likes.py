import configparser
import logging.config

import redis
import hug
import sqlite_utils
import json

likes = redis.Redis(host='localhost', port=6379, db=0)
config = configparser.ConfigParser()
config.read("./etc/api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)

@hug.directive()
def sqlite(section="sqlite", key="dbfile", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

@hug.directive()
def timelinesdb(section="timelinesdb", key="dbfile", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)


@hug.post("/likes/")
def likePosts(db:timelinesdb, postID:hug.types.text, username:hug.types.text):

    timelines = db["posts"]
    listOfPosts = likes.lrange(username, 0, -1)

    if not postID.encode("utf-8") in listOfPosts:
        likes.rpush(username, postID)
        likes.incr("postID:"+postID)
        return (username + " has successfully liked the post " + postID)
    else:
        likes.delete(username, postID)
        likes.decr("postID:"+postID)
        return (username + " has successfully unliked the post " + postID)

@hug.get("/likesCount/")
def likeCount(db:timelinesdb, postID:hug.types.text):
    return likes.get("postID:"+postID)

@hug.get("/likedPosts/")
def likedPosts(db:timelinesdb, username:hug.types.text):
    timelines = db["posts"]
    postIDs = likes.lrange(username, 0, -1)
    values = str
    
    for i in range(len(values)):
        if i==0:
            values = "id = ?"
        else:
            values += " OR id = ?"
        
    return {"posts" : timelines.rows_where(values, postIDs)}

#     @hug.get("/posts/mypost/")
# def getUserTimeline(db:timelinesdb, username):
    
#     timelines = db["posts"]

#     return {"posts" : timelines.rows_where("username = ?", [username])}


# API call to flush the database
@hug.get("/flush/")
def flush():
        return ("This post has " + likes.flushdb() + " likes")



# .decode("utf-8") 