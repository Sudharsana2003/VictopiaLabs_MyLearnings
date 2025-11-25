import requests

endpoint = "http://localhost:8000/api/"

response = requests.post(endpoint, json={"title":"Hello World"})
print("STATUS:", response.status_code)
print("RAW:", response.text)
print("DICT:", response.json())
