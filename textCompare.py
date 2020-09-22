from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.textCompareDB
users = db["users"]


def user_exist(username):
    if users.find({"username": username}).count() == 0:
        return False
    else:
        return True


def correct_passwd(username, passwd):
    hashed_passwd = users.find({"username": username})[0]["passwd"]
    if bcrypt.hashpw(passwd.encode('utf8'), hashed_passwd) == hashed_passwd:
        return True
    else:
        return False


def count_token(username):
    token_number = users.find({"username": username})[0]["token"]
    return token_number


class register(Resource):
    def post(self):
        # Get posted data
        get_posted_data = request.get_json()
        username = get_posted_data["username"]
        passwd = get_posted_data["passwd"]
        hashed_passwd = bcrypt.hashpw(passwd.encode('utf8'), bcrypt.gensalt())

        # Check if valid user
        if user_exist(username):
            ret_json = {
                "Message": "Invalid username",
                "status code": 301
            }
            return jsonify(ret_json)

        # Store account information into database
        users.insert(
            {
                "username": username,
                "passwd": hashed_passwd,
                "token": 5
            })
        ret_json = {
            "Message": "Your account has been created",
            "status code": 200
        }
        return jsonify(ret_json)


class detect(Resource):
    def post(self):
        # Get posted data
        posted_data = request.get_json()
        username = posted_data["username"]
        passwd = posted_data["passwd"]
        text1 = posted_data["text1"]
        text2 = posted_data["text2"]

        # Validate user name
        if not user_exist(username):
            ret_json = {
                "Message": "Invalid username",
                "Status code": 301
            }
            return jsonify(ret_json)

        # Validate password
        if not correct_passwd(username, passwd):
            ret_json = {
                "Message": "Invalid password",
                "Status code": 302
            }
            return jsonify(ret_json)

        # Count current token number
        token_number = count_token(username)
        if token_number <= 0:
            ret_json = {
                "Message": "You do not have enough token",
                "Status code": 303
            }
            return jsonify(ret_json)

        # Compare two text
        nlp = spacy.load('en_core_web_sm')
        text01 = nlp(text1)
        text02 = nlp(text2)
        ratio = text01.similarity(text02)

        # Minus 1 token for the service
        users.update(
            {"username": username},
            {"$set":
                {"token": token_number - 1}
             }
                    )

        # Return result
        ret_json = {
            "Similarity": ratio,
            "Status code": 200
        }
        return jsonify(ret_json)


api.add_resource(register, "/register")
api.add_resource(detect, "/detect")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
