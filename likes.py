import configparser
import logging.config
import requests

import heapq
import redis
from requests.models import Response
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
def likePosts(postID:hug.types.text, username:hug.types.text):

    listOfPosts = likes.lrange(username, 0, -1)

    if not postID.encode("utf-8") in listOfPosts:
        likes.rpush(username, postID)
        if not postID.encode("utf-8") in likes.lrange("postsWithLikes", 0, -1):
            likes.rpush("postsWithLikes", postID)
        likes.incr("postID:"+postID)
        
        return (username + " has successfully liked the post " + postID)
    else:
        likes.delete(username, postID)
        likes.decr("postID:"+postID)
        return (username + " has successfully unliked the post " + postID)

@hug.get("/likesCount/")
def likeCount(postID:hug.types.text):
    return likes.get("postID:"+postID)

@hug.get("/likedPosts/")
def likedPosts(username:hug.types.text):

    postIDs = likes.lrange(username, 0, -1)
    result = {}
    

    for i in postIDs:
        response = requests.get('http://localhost/posts/' + i.decode("utf-8") )
        result[i.decode("utf-8")]=response.json()["post"]
    return result

@hug.get("/topPosts/")
def topPosts( number:hug.types.number):
    L = []
    range = likes.lrange("postsWithLikes", 0, -1)
    for i in range:
        response = requests.get('http://localhost:8000/likesCount/?postID=' + i.decode("utf-8") )
        L.append({i.decode("utf-8"), response})
    return L

# API call to flush the database
@hug.get("/flush/")
def flush():
        likes.flushdb()
        return "The database has been flushed"



# .decode("utf-8") 