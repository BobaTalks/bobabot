from flask import Flask, request, Response
import db as store

app = Flask(__name__)

db = store.init_db()

@app.route('/tags', methods=['GET', 'POST'])
def tags():
    if request.method == 'GET':
        res = store.read_tags(db)
        return res
    if request.method == 'POST':
        body = request.get_json()
        res = store.create_tag(db, body)
        return res

@app.route('/tags/<int:tag_id>', methods=['GET', 'DELETE'])
def tags_by_id(tag_id):
    if request.method == 'GET':
        res = store.read_tag_by_id(db,tag_id)
        return res
    if request.method == 'DELETE':
        res = store.delete_tag_by_id(db, tag_id)
        return res
        