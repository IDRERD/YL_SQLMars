from requests import delete

print(delete("http://localhost:5000/api/jobs/4").json())