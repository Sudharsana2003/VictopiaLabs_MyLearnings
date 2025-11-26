import requests

endpoint = "http://localhost:8000/api/products/12345678/"

response = requests.get(endpoint)
print(response.json())
