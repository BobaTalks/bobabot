from pymongo import MongoClient
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
    db.reviewers
    return db

def create_tags(db, data):
    db.tags.insert_one(data)
    return None

def read_tags(db):
    payload = dumps(db.tags.find())
    return payload

def create_reviewers(db, data):
    db.tags.insert_one(data)

def read_reviewers(db):
    payload = dumps(db.reviewers.find())
    return payload


