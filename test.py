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

response = requests.get(BASE + "pet/findByStatus", {"status":"SOLD"})
print(response)