from requests import get, post, delete
from pprint import pprint

pprint(get("http://localhost:5000/api/v2/jobs").json())
pprint(get("http://localhost:5000/api/v2/jobs/1").json())
pprint(get("http://localhost:5000/api/v2/jobs/111111").json())
print(delete("http://localhost:5000/api/v2/jobs/1").json())
print(delete("http://localhost:5000/api/v2/jobs/111111").json())
print(post("http://localhost:5000/api/v2/jobs", json={
    "team_leader": 1,
    "job": "Test job resource",
    "work_size": 24,
    "collaborators": "1",
    "is_finished": True
}).json())
print(post("http://localhost:5000/api/v2/jobs", json={}).json())