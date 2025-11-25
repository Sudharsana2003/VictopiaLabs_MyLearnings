import requests

endpoint = "http://localhost:8000/api/products/1/update/"

data = {
    "title": "Updated Product Title",
    "content": "Updated content for this product",
    "price": 499
}

response = requests.put(endpoint, json=data)
print(response.status_code)
print(response.json())
