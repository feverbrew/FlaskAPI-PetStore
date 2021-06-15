import requests

BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE + "pet/1", {"name":"Billy Jean", "photoUrls":["dogceo.com","dog2.com"], "status":"SOLD"})
print(response.json())

response = requests.post(BASE + "pet", {"id":2, "name":"Buster Brown", "photoUrls":["sadface.jpeg"], "status":"SOLD"})
print(response.json())

response = requests.get(BASE + "pet/1")
print(response.json())