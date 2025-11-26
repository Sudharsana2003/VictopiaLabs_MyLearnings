import requests

product_id = 1   # change this to the id you want to delete

endpoint = f"http://localhost:8000/api/products/10/delete/"

response = requests.delete(endpoint)

print(response.status_code)
try:
    print(response.json())
except:
    print("No JSON response")
