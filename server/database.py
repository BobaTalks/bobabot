from pymongo import MongoClient, errors
import json
from bson.json_util import dumps
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.environ["MONGO_URI"]
DATABASE_NAME = os.environ["DATABASE_NAME"]


def initialize_database():
    client = MongoClient(MONGO_URI)
    try:
        client.tags.command("ping")
    except errors.ConnectionFailure:
        print("Server not available")

    database = client[f"{DATABASE_NAME}"]

    # create tags collection if it does not already exist
    database.tags

    database.tags.create_index("snowflake_id", unique=True)
    # expected structure for a tag:
    # {
    #     _id: 2389237842, #auto-generated id given by mongodb
    #     snowflake_id: 273723874873, #id given to tag in discord api
    #     tag_name: 'Software Engineering', #the name(maybe abbreviation) of the tag
    #     subscribers: [4367482348, 4372894729] #array of ids subscribed to tag
    # }
    return database


# create_tag inserts a tag object into the database
def create_tag(db, data):
    try:
        db.tags.insert_one(data)
    except errors.DuplicateKeyError:
        return ({"Error": "Resource Already Exists"}, 400)
    return ("Created", 201)


# read_tags retrieves all of the tag objects in the database
def read_tags(db):
    # get mongo db object and convert to string
    mongo_string = dumps(db.tags.find())

    # encode string to json
    payload = json.loads(mongo_string)
    return (payload, 200)


# read_tag_by_id retrieves the tag object with the given id
def read_tag_by_id(db, id):
    mongo_string = dumps(db.tags.find_one({"snowflake_id": id}))
    if mongo_string == "null":
        return ({"Error": "Resource Does Not Exist"}, 404)
    payload = json.loads(mongo_string)
    return (payload, 200)


# delete_tag_by_id removes a tag from the database with the given id
def delete_tag_by_id(db, id):
    mongo_string = dumps(db.tags.find_one_and_delete({"snowflake_id": id}))
    if mongo_string == "null":
        return ({"Error": "Resource Does Not Exist"}, 404)
    return ("Delete Successful", 200)


# create_subscriber inserts a subscriber id into the database for the tag with the given tag id
def create_subscriber(db, tag_id, subscriber_id):
    query_results = db.tags.update_one(
        {"snowflake_id": tag_id}, {"$addToSet": {"subscribers": subscriber_id}}
    )
    # the query results when the id already exists within the array
    if query_results.modified_count == 0:
        return ({"Success": "Resource Already Exists"}, 200)
    return ({"Success": "Resource Created"}, 201)


# (IP) remove_subscriber removes a subscriber from a selected tag id in a database
def remove_subscriber_from_tag(db, tag_id, subscriber_id):
    query_results = db.tags.update_one(
        {"snowflake_id": tag_id}, {"$pull": {"subscribers": subscriber_id}}
    )
    if query_results.modified_count == 0:
        return ({"Error": "Subscriber Does Not Exist"}, 404)
    return ({"Success": "Delete Successful"}, 200)


# read_subscribers retrieves the array of subscribers from the tag object with the given tag id
def read_subscribers(db, tag_id):
    mongo_string = dumps(db.tags.find_one({"snowflake_id": tag_id})["subscribers"])
    if mongo_string == "null":
        return ({"Error": "Resource Does Not Exist"}, 404)
    payload = json.loads(mongo_string)
    return (payload, 200)
