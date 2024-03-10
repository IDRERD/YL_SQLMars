from requests import delete, get

print(get("http://localhost:5000/api/jobs").json())  # Jobs before test requests
print("----------------------------------")

print(delete("http://localhost:5000/api/jobs/3").json())  # Correct request
print(delete("http://localhost:5000/api/jobs/first_job").json())  # job_id can't be str type
print(delete("http://localhost:5000/api/jobs/1111111").json())  # No job with id 1111111 in database

print("----------------------------------")
print(get("http://localhost:5000/api/jobs").json())  # Jobs after test requests