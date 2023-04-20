from flask import Flask, request, Response
import database

# instantiate flask server
app = Flask(__name__)

# connect to the database
conn = database.initialize_database()

# tags routes the /tags endpoint
@app.route("/tags", methods=["GET", "POST"])
def tags():
    if request.method == "GET":
        get_tags_response = database.read_tags(conn)
        return get_tags_response
    if request.method == "POST":
        body = request.get_json()
        post_tags_response = database.create_tag(conn, body)
        return post_tags_response


# tag_by_id routes the /tags/:id endpoint
@app.route("/tags/<int:tag_id>", methods=["GET", "DELETE"])
def tag_by_id(tag_id):
    if request.method == "GET":
        get_tag_response = database.read_tag_by_id(conn, tag_id)
        return get_tag_response
    if request.method == "DELETE":
        delete_tag_response = database.delete_tag_by_id(conn, tag_id)
        return delete_tag_response
