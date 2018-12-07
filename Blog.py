import json
from pymongo import MongoClient
from bson import ObjectId
from flask import Flask, request
app = Flask(__name__)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

client = MongoClient('mongodb://admin:abc@bigblogbuster-shard-00-00-avps1.mongodb.net:27017,bigblogbuster-shard-00-01-avps1.mongodb.net:27017,bigblogbuster-shard-00-02-avps1.mongodb.net:27017/blogdb?ssl=true&replicaSet=BigBlogBuster-shard-0&authSource=admin&retryWrites=true', 27017)

blog_db = client['blog-db']

users = []
post = []

@app.route("/users", methods=["POST", "GET"])
def user_list():
    if request.method == 'GET':
        user_coll = blog_db['user']
        print(list(user_coll.find()))
        return JSONEncoder().encode(list(user_coll.find()))
    else:
        usr = {
            "UserName": request.get_json()['UserName'],
            "Name": request.get_json()['Name'],
            "PassWord": request.get_json()['Password'],
            "Age": '0'
        }
        user_coll = blog_db['user']
        user_coll.insert_one(usr)
        return "Done."

@app.route("/users/<username>", methods=["GET", "DELETE", "PUT"])
def blog_User_list(username):
    if request.method == 'GET':
        user_coll = blog_db['user']
        return JSONEncoder().encode(user_coll.find_one({"UserName":username}))
    elif request.method == 'DELETE':
        user_coll = blog_db['user']
        user_coll.delete_one({"UserName": username})
        return "Done"
    else:
        user_coll = blog_db['user']
        user_coll.update({"UserName": username},{"$set": request.get_json()})
        return "Done"

@app.route("/posts", methods=["POST", "GET"])
def post_list():
    if request.method == 'GET':
        post_coll = blog_db['posts']
        print(list(post_coll.find()))
        return JSONEncoder().encode(list(post_coll.find()))
    else:
        pst = {
            "ID": request.get_json()['ID'],
            "Title": request.get_json()['Title'],
            "Body": request.get_json()['Body'],
            "Userid": request.get_json()['Userid'],
            "Age": '0',
            "Comment": []
            }
        post_coll = blog_db['posts']
        post_coll.insert_one(pst)
        return "Done."

@app.route("/posts/<ID>", methods=["GET", "DELETE", "PUT"])
def blog_post_list(ID):
    if request.method == 'GET':
        post_coll = blog_db['posts']
        return JSONEncoder().encode(post_coll.find_one({"ID":ID}))
    elif request.method == 'DELETE':
        post_coll = blog_db['posts']
        post_coll.delete_one({"ID": ID})
        return "Done"
    else:
        post_coll = blog_db['posts']
        post_coll.update({"ID": ID},{"$set": request.get_json()})
        return "Done"

@app.route("/posts/<ID>/comments", methods=["POST"])
def blog_comment_List(ID):
    post_coll = blog_db['posts']
    post_coll.update({"ID": ID}, {"$push": {"Comments":{request.get_json()['IDC'],request.get_json()['body'], request.get_json()['userid'] }}})

@app.route("/posts/<ID>/comments/<commentID>", methods=["GET", "DELETE"])
def blog_comment_list_one(ID, commentID):
    if request.method == 'GET':
        post_coll = blog_db['posts']
