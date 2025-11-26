import requests
from requests.auth import HTTPBasicAuth

# The product ID you want to delete
product_id = 10

# Endpoint URL
endpoint = f"http://localhost:8000/api/products/10/delete/"

# Your superuser credentials
auth = HTTPBasicAuth('sudharsana', 'root')

# Make DELETE request
response = requests.delete(endpoint, auth=auth)

# Print response
print("Status code:", response.status_code)
try:
    print("Response JSON:", response.json())
except:
    print("No JSON response (likely 204 No Content)")
