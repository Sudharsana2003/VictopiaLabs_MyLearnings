import requests
import json
from getpass import getpass
import datetime 

# --- Configuration ---
HOST = "http://127.0.0.1:8000"
AUTH_ENDPOINT = f"{HOST}/api/auth/"
LIST_ENDPOINT = f"{HOST}/api/products/"
CREATE_ENDPOINT = f"{HOST}/api/products/"
DETAIL_ENDPOINT = f"{HOST}/api/products/{{product_id}}/" 
UPDATE_ENDPOINT = f"{HOST}/api/products/{{product_id}}/update/"
DELETE_ENDPOINT = f"{HOST}/api/products/{{product_id}}/delete/"

# --- 1. Get Credentials ---
print("--- Authentication ---")
username = input("Enter username: ")
password = getpass("Enter password: ")

# --- 2. Request the Auth Token (Login) ---
auth_response = requests.post(
    AUTH_ENDPOINT,
    json={'username': username, 'password': password}
)

if auth_response.status_code == 200:
    token = auth_response.json().get('token')
    print(f"\nTOKEN RECEIVED: {token}")
else:
    print(f"\nAUTHENTICATION FAILED. Status Code: {auth_response.status_code}")
    print(auth_response.json())
    exit()

# --- 3. Define Authenticated Headers ---
HEADERS = {
    "Authorization": f"Token {token}" 
}

# --- 4. Test VIEW (List All Products) ---
print("\n--- Testing VIEW (List) ---")
view_response = requests.get(LIST_ENDPOINT, headers=HEADERS)

if view_response.status_code == 200:
    data = view_response.json()
    product_count = len(data)
    
    print(f"VIEW SUCCESS (200). Found {product_count} products.")
    print("--- FULL PRODUCT LIST (JSON) ---")
    print(json.dumps(data, indent=4)) 
    print("--------------------------------")
    print("Please use one of the displayed IDs for Update/Delete tests.")
else:
    print(f"VIEW FAILED ({view_response.status_code}). Detail: {view_response.json().get('detail')}")

# --- 5. Test ADD (Create New Product) ---
print("\n--- Testing ADD (Create) ---")
if input("Do you want to create a new product? (y/n): ").lower() == 'y':
    new_product_title = input("  Enter Title: ")
    new_product_price = input("  Enter Price: ")
    
    try:
        new_product_data = {
            'title': new_product_title,
            'price': float(new_product_price)
        }
    except ValueError:
        print("ADD SKIPPED: Invalid price entered.")
        
    else:
        create_response = requests.post(CREATE_ENDPOINT, headers=HEADERS, json=new_product_data)
        if create_response.status_code in [200, 201]:
            new_product_id = create_response.json().get('id', 'N/A')
            print(f"ADD SUCCESS ({create_response.status_code}). New Product ID: {new_product_id}")
        else:
            print(f"ADD FAILED ({create_response.status_code}). Detail: {create_response.json().get('detail')}")
else:
    print("Add action skipped.")
    
# --- 6. Test UPDATE (Update a specific product) ---
print(f"\n--- Testing UPDATE ---")
if input(f"Do you want to update a product? (y/n): ").lower() == 'y':
    
    update_id_input = input("  Enter the ID of the product to UPDATE: ")
    
    try:
        update_product_id = int(update_id_input)
    except ValueError:
        print("Update action skipped: Invalid ID entered.")
        
    else:
        # 1. Fetch Existing Record
        detail_url = DETAIL_ENDPOINT.format(product_id=update_product_id)
        detail_response = requests.get(detail_url, headers=HEADERS)
        
        if detail_response.status_code == 200:
            existing_data = detail_response.json()
            print("\n--- Current Product Data (Before Update) ---")
            print(json.dumps(existing_data, indent=4))
            print("------------------------------------------")
            
            # 2. Prompt for New Content
            current_title = existing_data.get('title', 'N/A').split(' at ')[0].strip()
            
            new_title = input(f"  Enter NEW Title (Current: '{current_title}'): ")
            new_content = input(f"  Enter NEW Content (Current: '{existing_data.get('content')}'): ")
            
            # 3. Construct the Update Payload
            update_data = {
                'title': new_title if new_title else existing_data.get('title'),
                'content': new_content if new_content else existing_data.get('content'),
                'title': f'{new_title if new_title else existing_data.get("title")} updated by {username} at {datetime.datetime.now():%H:%M}',
                'price': existing_data.get('price')
            }
            
            # 4. Execute the PUT Request
            update_url = UPDATE_ENDPOINT.format(product_id=update_product_id)
            update_response = requests.put(update_url, headers=HEADERS, json=update_data)

            if update_response.status_code == 200:
                print(f"\nUPDATE SUCCESS (200). Product {update_product_id} updated.")
            else:
                print(f"\nUPDATE FAILED ({update_response.status_code}). Detail: {update_response.json().get('detail')}")
                
        elif detail_response.status_code == 404:
            print(f"Update action skipped: Product ID {update_product_id} not found.")
        else:
            print(f"Update action skipped: Failed to fetch data (Status {detail_response.status_code}). Detail: {detail_response.json().get('detail')}")
else:
    print("Update action skipped.")

# --- 7. Test DELETE (Delete a specific product) ---
print(f"\n--- Testing DELETE ---")
if input(f"Do you want to DELETE a product? (y/n): ").lower() == 'y':
    
    delete_id_input = input("  Enter the ID of the product to DELETE: ")
    
    try:
        delete_product_id = int(delete_id_input)
    except ValueError:
        print("Delete action skipped: Invalid ID entered.")
        
    else:
        delete_url = DELETE_ENDPOINT.format(product_id=delete_product_id)
        delete_response = requests.delete(delete_url, headers=HEADERS)

        if delete_response.status_code == 204:
            print(f"DELETE SUCCESS (204 No Content). Product {delete_product_id} deleted.")
        else:
            print(f"DELETE FAILED ({delete_response.status_code}). Detail: {delete_response.text}")
else:
    print("Delete action skipped.")