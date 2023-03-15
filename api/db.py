from pymongo import MongoClient, errors
import json
from bson.json_util import dumps
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.environ['MONGO_URI']

def init_db():
    client = MongoClient(MONGO_URI)
    db = client.test
    
    #create tags and reviewers collections if they do not already exist
    db.tags
    
    db.tags.create_index("snowflake_id", unique=True)
    # expected structure for a tag:
    # {
    #     _id: 2389237842, #auto-generated id given by mongodb
    #     snowflake_id: 273723874873, #id given to tag in discord api
    #     tag_name: 'Software Engineering', #the name(maybe abbreviation) of the tag
    #     subscribers: [4367482348, 4372894729] #array of ids subscribed to tag
    # }

    return db

def create_tag(db, data):
    try:
        db.tags.insert_one(data)
    except errors.DuplicateKeyError:
        duplicate_response = "Resource Already Exists"
        return (duplicate_response, 400)
    return ("Created", 201)

def read_tags(db):
    # get mongo db object and convert to string
    mongo_string = dumps(db.tags.find())
    
    # encode string to json
    payload = json.loads(mongo_string)
    return payload

def read_tag_by_id(db, id):
    mongo_string = dumps(db.tags.find_one({'snowflake_id': id}))
    if mongo_string == "null":
        return ({"Error": "Resource Does Not Exist"}, 404)
    payload = json.loads(mongo_string)
    return payload

def delete_tag_by_id(db, id):
    mongo_string = dumps(db.tags.find_one_and_delete({'snowflake_id': id}))
    if mongo_string == "null":
        return ({"Error": "Resource Does Not Exist"}, 404)
    return ("Delete Successful",200)

