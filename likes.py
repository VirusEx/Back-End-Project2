import configparser
import logging.config

import redis
import hug
import sqlite_utils

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
def likePosts(db:timelinesdb, postID, username:hug.types.text):

    timelines = db["posts"]
    listOfPosts = likes.lrange(username, 0, -1)

    if not postID in listOfPosts:
        likes.rpush(username, postID)
        likes.incr(postID)
        return (username + " liked the post")
  
    return {"Error: You already liked this posts"}

        

# .decode("utf-8") 