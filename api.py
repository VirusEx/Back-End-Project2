# Science Fiction Novel API - Hug Edition
#
# Adapted from "Creating Web APIs with Python and Flask"
# <https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask>.
#

import configparser
import logging.config

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


# Routes
#hug.get(examples='username=Timothy&email=abc@abc.com&password=123')
@hug.post("/users/", status=hug.falcon.HTTP_201)
def create_users(
    response,
    username: hug.types.text,
    email: hug.types.text,
    password: hug.types.text,
    db: sqlite,
):
    users = db["users"]

    user = {
        "username": username,
        "email": email,
        "password": password,
    }

    try:
        users.insert(user)
        user["username"] = users.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    response.set_header("Location", f"/users/{user['username']}")
    return user

@hug.get("/users/")
def authenticateUser(request, db:sqlite, username:hug.types.text, password):

    users = db["users"]
   

    return {"users" : users.rows_where("username = \"", username, "\"") }

