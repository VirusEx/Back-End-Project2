# Science Fiction Novel API - Hug Edition
#
# Adapted from "Creating Web APIs with Python and Flask"
# <https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask>.
#

import configparser
import logging.config
from typing import Optional

import hug
import sqlite_utils

# Load configuration
#
config = configparser.ConfigParser()
config.read("./etc/api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)


# Arguments to inject into route functions
#
@hug.directive()
def sqlite(section="sqlite", key="dbfile", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)


@hug.directive()
def log(name=__name__, **kwargs):
    return logging.getLogger(name)

@hug.directive()
def timelinesdb(section="timelinesdb", key="dbfile", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

# Routes
#hug.get(examples='username=Timothy&email=abc@abc.com&password=123')
@hug.get("/posts/mypost/")
def getUserTimeline(db:timelinesdb, username):
    
    timelines = db["posts"]

    return {"posts" : timelines.rows_where("username = ?", [username])}

@hug.get("/posts/allpost")
def getPublicTimeline(db:timelinesdb):
    timelines = db["posts"]
    return {"posts" : timelines.rows_where()}

# following is a list of following ID from client
@hug.get("/posts/home")
def getHomeTimeline(db:timelinesdb, followings):
    
    timelines = db["posts"]
    values = str
    for i in range(len(followings)):
        if i==0:
            values = "user_id = ?"
        else:
            values += " OR user_id = ?"

    return {"posts" : timelines.rows_where(values, followings)}


#TODO FINISH THIS
@hug.post("/posts/")
def postTweet(
    response,
    username: hug.types.text,
    user_id: hug.types.number,
    text: hug.types.text,
    db: timelinesdb,
):

    timelines = db["posts"]
    post = {
        "username":username,
        "user_id":user_id,
        "text":text
    }

    try:
        timelines.insert(post)
        post["id"] = timelines.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    #response.set_header("Location", f"/followers/{follower['id']}")
    return post