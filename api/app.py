from flask import Flask, request, Response
from db import init_db, create_tags, read_tags, create_reviewers, read_reviewers
from bson.json_util import dumps

app = Flask(__name__)

db = init_db()

@app.route('/tags', methods=['GET', 'POST'])
def tags():
    if request.method == 'GET':
        obj = read_tags(db)
        return obj
    if request.method == 'POST':
        body = request.get_json()
        create_tags(db, body)
        return "Created", 201

@app.route('/reviewers', methods=['GET','POST'])
def reviewers():
    if request.method == 'GET':
        obj = read_reviewers(db)
        return obj
    if request.method == 'POST':
        body = request.get_json()
        create_reviewers(db, body)
        return "Created", 201