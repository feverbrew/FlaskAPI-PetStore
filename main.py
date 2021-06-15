from flask import Flask, abort, request
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

img_arg = reqparse.RequestParser()
img_arg.add_argument("photoUrl", type=str)

status_arg = reqparse.RequestParser()
status_arg.add_argument("statuses", type=Status, action = 'append')

pets = {}

def pet_id_dne(id):
    if id not in pets:
        abort(400, "ID does not exist!")

def pet_id_exists(id):
    if id in pets:
        abort(405, "ID already exists!")

class Pet(Resource):
    def put(self):
        id = pets_args.args[0]
        pet_id_dne(id)
        pets[id] = pets_args.parse_args()
        return pets[id]
    def post(self):
        id = pets_args.args[0]
        pet_id_exists(id)
        pets[id] = pets_args.parse_args()
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
        pets[id]['photoUrls'].append(img_arg.args[0]) # Pretty sure this is broken, check parser more thouroughly. Maybe need to use parse args? Or its possible there is something else wrong here.
        #won't let me print the json response (probably because this isn't actually an image from the way I'm doing it)
        return 'Picture successfully uploaded!'

class StatusFilter(Resource):
    def get(self):
        filteredpets = {}
        for pet in pets:
            if pet['status'] in status_arg.args[0]: # Almost certainly broken as well lol
                filteredpets[pet.id] = pet
        return filteredpets



api.add_resource(Pet, "/pet")
api.add_resource(PetID, "/pet/<int:id>")
api.add_resource(PetIDImage, "/pet/<int:id>/uploadImage")
api.add_resource(StatusFilter, "/pet/findByStatus")


if __name__ == "__main__":
    app.run(debug=True)