import requests
from requests.api import request

BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE + "pet/1", {"name":"Billy Jean", "photoUrls":["dogceo.com","dog2.com"], "status":"SOLD"})
print(response.json())

response = requests.post(BASE + "pet", {"id":2, "name":"Buster Brown", "photoUrls":["sadface.jpeg"], "status":"PENDING"})
print(response.json())

response = requests.post(BASE + "pet/1/uploadImage", {"photoUrl":"url.url.pog"})

response = requests.get(BASE + "pet/1")
print(response.json())

response = requests.get(BASE + "pet/findByStatus", {"statuses":"SOLD"})
print(response.json())

response = requests.post(BASE + "/user", {"id":1, "username":"feverbrew", "firstName":"Lucas", "lastName":"Culley", "email":"feverbrew@gmail.com", "password":"12345", "status":1})
print(response.json())

response = requests.get(BASE + "/user/login", {"username":"feverbrew", "password":"nottherightpword"})
print(response.json())

response = requests.get(BASE + "/user/login", {"username":"feverbrew", "password":"12345"})
print(response.json())

response = requests.get(BASE + "/user/logout")
print(response.json())

response = requests.post(BASE + "/store/order", {"id":1, "petId":2, "quantity":2, "shipdate":"June 2019", "status":"DELIVERED", "complete":True})
print(response.json())

response = requests.get(BASE + "/store/inventory")
print(response.json())

# response = requests.post(BASE + "/user/createWithList", {{"id":1, "username":"feverbrew", "firstName":"Lucas", "lastName":"Culley", "email":"feverbrew@gmail.com", "password":"12345", "status":1}, 
#                                                         {"id":2, "username":"mumpyman", "firstName":"Kyle", "lastName":"Culley", "email":"mumpy@gmail.com", "password":"123456", "status":1}, 
#                                                         {"id":3, "username":"hannahcarrot", "firstName":"Hannah", "lastName":"Culley", "email":"carrot@gmail.com", "password":"12345678", "status":1}})
# print(response.json())