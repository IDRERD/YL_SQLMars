from requests import get, post, delete
from pprint import pprint

pprint(get("http://localhost:5000/api/v2/users").json())
pprint(get("http://localhost:5000/api/v2/users/1").json())
pprint(get("http://localhost:5000/api/v2/users/111111").json())
print(delete("http://localhost:5000/api/v2/users/1").json())
print(delete("http://localhost:5000/api/v2/users/111111").json())
print(post("http://localhost:5000/api/v2/users", json={
    "surname": "Watney",
    "name": "Mark",
    "age": 24,
    "position": "Cap",
    "speciality": "biologist",
    "address": "module_2",
    "email": "mwatney@mars.org"
}).json())
print(post("http://localhost:5000/api/v2/users", json={}).json())