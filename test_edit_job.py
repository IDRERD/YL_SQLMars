from requests import post, get
from pprint import pprint

pprint(get("http://localhost:5000/api/jobs/4").json())
print("-------------------------")

print(post("http://localhost:5000/api/jobs/4", json={
    'team_leader': 1,
    'job': 'Edited job1',
    'work_size': 24,
    'collaborators': '1, 2',
    # 'start_date': datetime.datetime.now(),
    # 'end_date': (datetime.datetime.now() + datetime.timedelta(days=1)),
    'is_finished': False
}).json())

print("-------------------------")
pprint(get("http://localhost:5000/api/jobs/4").json())