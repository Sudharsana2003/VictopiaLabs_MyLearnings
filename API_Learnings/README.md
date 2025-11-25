
# 🚀 **Django REST Framework — Complete API Project Documentation**

A comprehensive, production-ready backend API built with **Django** and **Django REST Framework (DRF)**.
This project serves as a full learning + reference guide covering:

✔ CRUD operations
✔ Authentication (JWT + Token + Session)
✔ Permissions, Mixins, Generics
✔ CORS
✔ Pagination
✔ Searching with Q-objects
✔ Frontend integration

---

# 📌 **Table of Contents**

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Project Setup](#project-setup)
4. [Getting Started](#getting-started)
5. [HTTP Request Lifecycle](#http-request-lifecycle)
6. [Models & Serializers](#models--serializers)
7. [API Flow — GET & POST](#api-flow--get--post)
8. [Generic Views](#generic-views)
9. [Mixins](#mixins)
10. [Permissions & Groups](#permissions--groups)
11. [JWT Authentication (Deep Dive)](#jwt-authentication-deep-dive)
12. [Frontend Integration (HTML Test Client)](#frontend-integration-html-test-client)
13. [DRF Default Settings](#drf-default-settings)

---

# 🧩 **1. Project Overview**

This project demonstrates real-world, scalable API development, including:

* CRUD operations on **Product** model
* Custom serializer logic
* Permission-based access control
* Token & JWT authentication
* Pagination, validation, searching
* Frontend test client using pure HTML + JS

---

# 🛠 **2. Tech Stack**

| Category  | Component                     |
| --------- | ----------------------------- |
| Language  | Python 3.x                    |
| Framework | Django, Django REST Framework |
| Auth      | SimpleJWT, DRF TokenAuth      |
| Utility   | django-cors-headers, requests |

---

# ⚙️ **3. Project Setup**

### Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```
<img width="546" height="219" alt="image" src="https://github.com/user-attachments/assets/520e02f4-24f0-4286-9ce0-bfb5959abfe7" />


### Install Dependencies

```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers requests
```
<img width="975" height="401" alt="image" src="https://github.com/user-attachments/assets/8f948e20-2bc4-4f2f-820c-925e32b41966" />

### Create Project & App

```bash
django-admin startproject cfehome .
python manage.py startapp api
```

### Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
<img width="975" height="474" alt="image" src="https://github.com/user-attachments/assets/54ea8641-2b6b-47a1-98fa-8226d41c9eb9" />

### Create Superuser

```bash
python manage.py createsuperuser
```
<img width="778" height="246" alt="image" src="https://github.com/user-attachments/assets/508e1a72-1aad-4f86-91d9-c060d77d2f72" />
<img width="793" height="393" alt="image" src="https://github.com/user-attachments/assets/e853344d-20b9-47a6-a217-ab104de6b096" />

## Stafff User created by SuperUser
<img width="975" height="474" alt="image" src="https://github.com/user-attachments/assets/6df8a949-00a7-4132-88d6-c21da6f6ccd7" />



---

# 🚀 **4. Getting Started**

### Run Development Server

```bash
python manage.py runserver
```

Your API is now live at:

```
http://127.0.0.1:8000/
```

---

# 🔄 **5. HTTP Request Lifecycle**

| Step | Component   | Description                         |
| ---- | ----------- | ----------------------------------- |
| 1    | Client      | Sends HTTP request                  |
| 2    | Django URLs | `path('api/', include('api.urls'))` |
| 3    | DRF View    | Validates method + auth             |
| 4    | Serializer  | Converts data JSON ↔ Python ↔ Model |
| 5    | Response    | Returns JSON to frontend            |
| 6    | Client      | Reads response                      |

---

# 🧱 **6. Models & Serializers**

## Model (Database Fields)

```python
title = models.CharField(...)
price = models.DecimalField(...)
```

## Serializer (API Fields)

```python
sale_price = serializers.SerializerMethodField(read_only=True)
```

### Computed Fields

```python
def get_sale_price(self, obj):
    return "%.2f" % (obj.price * 0.8)   # 20% discount
```
<img width="975" height="507" alt="image" src="https://github.com/user-attachments/assets/6c15b15e-33cb-48d4-88cf-1719d3e4c935" />


---

# 🔁 **7. API Flow — GET & POST**

### GET Flow

1. Fetch instance
2. Serialize instance → Python dict
3. Return JSON

### POST Flow

1. Receive JSON from client
2. Validate via serializer
3. Save to DB
4. Return serializer data

```
JSON → Serializer → Model  
Model → Serializer → JSON
```

---

# 📚 **8. Generic Views**

DRF provides powerful CRUD shortcuts:

### List & Create

```python
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

### Retrieve & Update

```python
class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

---

# 🧩 **9. Mixins**

Mixins allow custom combinations:

```python
class ProductMixinView(
    Mixins.CreateModelMixin,
    Mixins.ListModelMixin,
    GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

---

# 🔐 **10. Permissions & Groups**

### User Levels

| Type                    | Meaning          |
| ----------------------- | ---------------- |
| Regular User            | Basic access     |
| Staff (`is_staff=True`) | Admin panel      |
| Superuser               | Full permissions |

### Group-Based Permissions

Example group:
**ProductEditors**

Permissions:

* `add_product`
* `change_product`
* `view_product`
* `delete_product` (optional)

### Custom Mixin for Staff

```python
class StaffEditorPermissionMixin:
    permission_classes = [IsAdminUser, IsStaffEditorPermission]
```

---

# 🔒 **11. JWT Authentication (Deep Dive)**

JWT provided by **djangorestframework-simplejwt**.

### Endpoints Provided

| Purpose              | Endpoint              |
| -------------------- | --------------------- |
| Get access + refresh | `/api/token/`         |
| Refresh access token | `/api/token/refresh/` |

### Example Response

```json
{
  "refresh": "refresh-token-string",
  "access": "access-token-string"
}
```

### Sending JWT With Request

```
Authorization: Bearer <access_token>
```

### Why JWT?

✔ Stateless → scalable
✔ Faster than DB token lookup
✔ Supports Refresh Token
✔ Perfect for frontend apps

---

<img width="975" height="518" alt="image" src="https://github.com/user-attachments/assets/fe233349-a949-405d-bc6f-08732ae6f773" />

# 🌐 **12. Frontend Integration (HTML Test Client)**

You created a local HTML client (e.g., `8111.html`) to test:

✔ Login
✔ Token retrieval
✔ Authenticated GET/POST
✔ CORS policies

<img width="975" height="346" alt="image" src="https://github.com/user-attachments/assets/9e5babf8-4884-485d-9f8d-ced1ed31443c" />


### Example JavaScript Flow

```javascript
fetch("http://127.0.0.1:8000/api/token/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
        "username": "admin",
        "password": "admin123"
    })
})
.then(res => res.json())
.then(data => {
    localStorage.setItem("access", data.access);
});
```

### Updating Auth Header

```javascript
headers: {
    "Authorization": "Bearer " + localStorage.getItem("access")
}
```

This HTML client helps you test APIs **without React/Vue**.

---

# ⚙️ **13. DRF Default Settings**

Your project uses:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 5
}
```

✔ JWT as primary auth
✔ Anonymous users: READ only
✔ Pagination enabled globally

---
