from flask import Flask, request, Response
import db

app = Flask(__name__)

#connect to the database
conn = db.init_db()

@app.route('/tags', methods=['GET', 'POST'])
def tags():
    if request.method == 'GET':
        res = db.read_tags(conn)
        return res
    if request.method == 'POST':
        body = request.get_json()
        res = db.create_tag(conn, body)
        return res

@app.route('/tags/<int:tag_id>', methods=['GET', 'DELETE'])
def tags_by_id(tag_id):
    if request.method == 'GET':
        res = db.read_tag_by_id(conn,tag_id)
        return res
    if request.method == 'DELETE':
        res = db.delete_tag_by_id(conn, tag_id)
        return res
        