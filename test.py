from requests import get, post

print(get("http://localhost:5000/api/jobs").json())
print(get("http://localhost:5000/api/jobs/1").json())
print(get("http://localhost:5000/api/jobs/11111").json())
print(get("http://localhost:5000/api/jobs/first_job").json())