import requests

endpoint = "http://localhost:8000/api/products/1/"

response = requests.get(endpoint)
print(response.json())

'''
print("STATUS:", response.status_code)
print("RAW:", response.text)
print("DICT:", response.json())

'''