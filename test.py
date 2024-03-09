from requests import get, post
import datetime

# print(get("http://localhost:5000/api/jobs").json())
# print(get("http://localhost:5000/api/jobs/1").json())
# print(get("http://localhost:5000/api/jobs/11111").json())
# print(get("http://localhost:5000/api/jobs/first_job").json())

print(post("http://localhost:5000/api/jobs", json={
    'team_leader': 1,
    'job': 'Test job1',
    'work_size': 24,
    'collaborators': '1, 2',
    # 'start_date': datetime.datetime.now(),
    # 'end_date': (datetime.datetime.now() + datetime.timedelta(days=1)),
    'is_finished': False
}).json())