from flask import Flask, abort, request, jsonify
from flask_restful import Api, Resource, reqparse
from enum import Enum

app = Flask(__name__)
api = Api(app)

class Status(str, Enum):
    AVAILABLE = "AVAILABLE"
    PENDING = "PENDING"
    SOLD = "SOLD"

pets_args = reqparse.RequestParser()
pets_args.add_argument("id",type=int)
pets_args.add_argument("name", type=str, required=True)
pets_args.add_argument("category", type={str:int, str:str})
pets_args.add_argument("photoUrls", type=str, action = 'append', required=True)
pets_args.add_argument("tags", type=str, action = 'append')
pets_args.add_argument("status", type=Status)

user_args = reqparse.RequestParser()
user_args.add_argument("id", type=int)
user_args.add_argument("username", type=str, required = True)
user_args.add_argument("firstName", type=str)
user_args.add_argument("lastName", type=str)
user_args.add_argument("email", type=str)
user_args.add_argument("password", type=str, required=True)
user_args.add_argument("phone", type=str)
user_args.add_argument("userStatus", type=int)

login_user = reqparse.RequestParser()
login_user.add_argument("username", type=str, required = True)
login_user.add_argument("password", type=str, required=True)

img_arg = reqparse.RequestParser()
img_arg.add_argument("photoUrl", type=str)

status_arg = reqparse.RequestParser()
status_arg.add_argument("statuses", type=Status, action = 'append')

userlist_args = reqparse.RequestParser()
userlist_args.add_argument("userlist", type=list)

pets = {}
users = {}
logged_in_users = []

def pet_id_dne(id):
    if id not in pets:
        abort(400, "ID does not exist!")

def pet_id_exists(id):
    if id in pets:
        abort(405, "ID already exists!")

def username_dne(username):
    if username not in users:
        abort(400, "ID does not exist!")

def username_exists(username):
    if username in users:
        abort(405, "ID already exists!")

def loggedIn(username):
    users[username].status = 1
    logged_in_users.append(username)

class Pet(Resource):
    def put(self):
        args = pets_args.parse_args()
        id = args.id
        pet_id_dne(id)
        pets[id] = args
        return pets[id]
    def post(self):
        args = pets_args.parse_args()
        id = args.id
        pet_id_exists(id)
        pets[id] = args
        return pets[id]

class PetID(Resource):
    def get(self, id):
        pet_id_dne(id)
        return pets[id]
    def post(self, id):
        pet_id_exists(id)
        pets[id] = pets_args.parse_args()
        pets[id].id = id
        return pets[id]
    def delete(self, id):
        pet_id_dne(id)
        pets.pop(id)
        return '', 204

class PetIDImage(Resource):
    def post(self, id):
        pet_id_dne(id)
        pets[id].photoUrls.append(img_arg.parse_args().photoUrl)
        return 'Picture successfully uploaded!'

class StatusFilter(Resource):
    def get(self):
        filteredpets = {}
        for id in pets:
            if pets[id].status in status_arg.parse_args().statuses:
                filteredpets[id] = pets[id]
        return jsonify(filteredpets)


class User(Resource):
    def post(self):
        args = user_args.parse_args()
        username = args.username
        username_exists(username)
        users[username] = args
        return users[username]

class UserList(Resource):
    def post(self):
        for i in userlist_args.parse_args():
            username_exists(i.username)
            users[i.username] = i
        return ''

class UserActions(Resource):
    def get(self, username):
        username_dne(username)
        return users[username]
    def put(self, username):
        username_dne(username)
        if users[username] in logged_in_users:
            users[username] = user_args.parse_args()
    def delete(self, username):
        username_dne(username)
        if users[username] in logged_in_users:
            users.pop(username)

class UserLogin(Resource):
    def get(self):
        login = login_user.parse_args()
        username_dne(login.username)
        if users[login.username].password == login.password:
            loggedIn(login.username)
        else:
            abort(401, "Invalid password!")

class UserLogout(Resource):
    def get(self):
        for user in logged_in_users:
            users[user].status = 0
        logged_in_users.clear()



api.add_resource(Pet, "/pet")
api.add_resource(PetID, "/pet/<int:id>")
api.add_resource(PetIDImage, "/pet/<int:id>/uploadImage")
api.add_resource(StatusFilter, "/pet/findByStatus")
api.add_resource(User, "/user")
api.add_resource(UserList, "/user/createWithList")
api.add_resource(UserActions, "/user/<string:username>")
api.add_resource(UserLogin, "/user/login")
api.add_resource(UserLogout, "/user/logout")


if __name__ == "__main__":
    app.run(debug=True)