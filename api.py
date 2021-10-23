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
@hug.post("/users/", status=hug.falcon.HTTP_201)
def create_users(
    response,
    username: hug.types.text,
    email: hug.types.text,
    password: hug.types.text,
    bio: hug.types.text,
    db: sqlite,
):
    users = db["users"]

    user = {
        "username": username,
        "email": email,
        "password": password,
        "bio": bio,
    }

    try:
        users.insert(user)
        user["id"] = users.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    response.set_header("Location", f"/users/{user['username']}")
    return user

@hug.get("/users/")
def authenticateUser(db:sqlite, username, password):

    users = db["users"]
   
    return {"users" : users.rows_where("username = ? AND password = ?", [username, password]) }

#TODO Delete this before submission
@hug.get("/allusers/")
def allusers(db:sqlite):
    return {"Users": db["users"].rows}

@hug.post("/followers/")
def addFollower(
    response,
    follower_id: hug.types.number,
    following_id: hug.types.number,
    db: sqlite,
):

    followers = db["followers"]
    follower = {
        "follower_id":follower_id,
        "following_id":following_id
    }

    try:
        followers.insert(follower)
        follower["id"] = followers.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_204
        return {"error": str(e)}

    response.set_header("Location", f"/followers/{follower['id']}")
    return follower

@hug.delete("/followers/")
def removeFollower(db:sqlite, response, follower_id:hug.types.number, following_id:hug.types.number):

    followers = db["followers"]

    try:
        followers.delete_where("follower_id = ? AND following_id = ?", [3,2])
    except Exception as e:
        response.status = hug.falcon.HTTP_704
        
    # return {"followers" : followers.rows_where("follower_id = ? AND following_id = ?", [follower_id, following_id])}
    return hug.falcon.HTTP_204

@hug.get("/following/")
def getFollowings (db:sqlite,  response, user_id:hug.types.number):

    followers = db["followers"]
    
    return followers.rows_where("follower_id = ?", [user_id], select='following_id')

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