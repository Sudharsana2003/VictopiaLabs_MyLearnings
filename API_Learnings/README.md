# *MY Django Learnings*

* CRUD operations
* DRF Serializers
* Token & JWT Authentication
* Permissions & Groups
* DRF Generic Views & Mixins
* Pagination & Filtering
* Q-Object Search
* ViewSets & Routers
* CORS handling
* Python & JavaScript API clients
---

# 📑 **Table of Contents**

1. Project Structure
2. Features
3. Installation & Setup
4. Virtual Environment
5. Installed Packages
6. Running the Server
7. API Architecture
8. Models & Serializers
9. API Endpoints (FBV, CBV, ViewSets)
10. Create / Update / Delete Flow
11. Authentication (Token + JWT)
12. Permissions & Groups
13. Pagination
14. Search API (Q-Objects)
15. CORS Handling
16. JS Client (Port 8111)
17. Python API Clients
18. Future Enhancements

---

# 📁 **1. Project Structure**

```
backend/
│
├── manage.py
├── db.sqlite3
│
├── cfehome/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── __init__.py
│
├── api/
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   └── admin.py
│
├── products/
│   ├── models.py
│   ├── serializers.py
│   ├── mixins.py
│   ├── validators.py
│   ├── permissions.py
│   ├── views.py
│   ├── viewsets.py
│   ├── urls.py
│   ├── migrations/
│   └── admin.py
│
├── search/
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   └── migrations/
│
├── js_client/
│   ├── index.html
│   └── client.js
│
└── py_client/
    ├── basic.py
    ├── create.py
    ├── list.py
    ├── update.py
    ├── delete.py
    ├── delete_with_user.py
    ├── token_test.py

venv/
requirements.txt
```

---

# ⭐ **2. Features**

* Full CRUD for Product API
* DRF Generic Views (Retrieve, Create, List, Update, Delete)
* DRF Mixins (custom permission mixins)
* ViewSets + Routers
* Authentication

  * Session
  * Token
  * JWT (SimpleJWT)
* Custom Permissions (role-based & group-based)
* Pagination (LimitOffset)
* Q-Object Dynamic Search
* Python scripts for API testing
* JavaScript client (Login + JWT + API calls)
* CORS enabled for port 8111

---

# 🛠️ **3. Installation & Setup**

Clone repo:

```bash
git clone <repo-url>
cd backend
```

---

# 🧪 **4. Create Virtual Environment**

```bash
python -m venv venv
venv\Scripts\activate
```
<img width="546" height="219" alt="image" src="https://github.com/user-attachments/assets/0bdd3042-187f-44b3-8b53-56576670bfbd" />

---

# 📦 **5. Install Required Packages**

```bash
pip install -r requirements.txt
```

or manually:

```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers requests
```
<img width="975" height="401" alt="image" src="https://github.com/user-attachments/assets/0e504615-21f4-402a-9ebf-72032274ac5b" />

---

# ▶️ **6. Run The Server**

```bash
python manage.py runserver
```

Default server:

```
http://127.0.0.1:8000/
```
<img width="816" height="385" alt="image" src="https://github.com/user-attachments/assets/0b6635b0-75cf-4ea9-b583-4e3784e02bc4" />

---

# 🏗️ **7. API Architecture**

```
Client → URL Router → View → Serializer → Model → DB
                            ↓
                       Response(JSON)
```
<img width="585" height="464" alt="image" src="https://github.com/user-attachments/assets/5cd87263-fe2f-4d39-837c-3adddb0fee53" />

---

# 🔧 **8. Models & Serializers**

### `models.py`

```python
class Product(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    public = models.BooleanField(default=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
```

### `serializers.py`

```python
class ProductSerializer(serializers.ModelSerializer):
    sale_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "title", "content", "price", "sale_price"]

    def get_sale_price(self, obj):
        return float(obj.price) * 0.8
```
<img width="975" height="474" alt="image" src="https://github.com/user-attachments/assets/0ad9ff1a-bac6-4c2d-86d6-5ec9f12adf68" />

---

# 📡 **9. API Endpoints**

## Function-Based View

```python
@api_view(["GET", "POST"])
def api_home(request):
    ...
```
<img width="684" height="393" alt="image" src="https://github.com/user-attachments/assets/00dfbb42-4e6b-430d-89ec-2ce5174ae7e6" />
<img width="975" height="561" alt="image" src="https://github.com/user-attachments/assets/4162125c-3466-4396-95ab-a1193f801251" />



## Generic Views

### List + Create

```python
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

### Retrieve

```python
class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

### Update

```python
class ProductUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

### Delete

```python
class ProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

## ViewSets + Routers

```python
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

Router:

```python
router.register("products", ProductViewSet)
```

---

# ✏️ **10. CRUD Flow**

### Create

```python
serializer = ProductSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
serializer.save()
```

### Update

```python
serializer = ProductSerializer(instance, data=request.data, partial=True)
serializer.is_valid(raise_exception=True)
serializer.save()
```
<img width="975" height="450" alt="image" src="https://github.com/user-attachments/assets/fe3bee2f-cea8-4ade-a87f-7794f80443f7" />


### Delete

```python
instance.delete()
```

---

# 🔐 **11. Authentication**

## Token Auth

```python
from rest_framework.authentication import TokenAuthentication
```

Generate token:

```bash
python manage.py drf_create_token <username>
```
<img width="975" height="480" alt="image" src="https://github.com/user-attachments/assets/68d1afed-6973-4dcd-bca0-8aac638afd59" />

Header format:

```
Authorization: Token <token>
```
<img width="975" height="370" alt="image" src="https://github.com/user-attachments/assets/6b76580a-96c9-41af-88b9-4a4f0e1a0a1e" />


## JWT Auth (SimpleJWT)

Install:

```bash
pip install djangorestframework-simplejwt
```

Add to settings:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ]
}
```

Endpoints:

* `/api/token/`
* `/api/token/refresh/`

Header:

```
Authorization: Bearer <access_token>
```
<img width="975" height="518" alt="image" src="https://github.com/user-attachments/assets/0fbc31f5-40bd-4815-94f0-224fc9498c90" />

---

# 🛂 **12. Permissions & Groups**

### Custom Permission Example

```python
class StaffEditorPermissionMixin:
    permission_classes = [IsStaffEditorPermission]
```
<img width="975" height="474" alt="image" src="https://github.com/user-attachments/assets/7ae7671d-719a-4ffd-ad9c-8749a05baf49" />


### Django Admin

* Add user
* Add group
* Assign permissions:

  * `add_product`
  * `view_product`
  * `change_product`
  * `delete_product`

<img width="746" height="291" alt="image" src="https://github.com/user-attachments/assets/f01f7bd9-ac08-4ca3-8ef2-1bfc43a4c800" />
<img width="975" height="287" alt="image" src="https://github.com/user-attachments/assets/153a4aa5-6b1b-46bb-9771-426d6e11de0e" />
<img width="759" height="397" alt="image" src="https://github.com/user-attachments/assets/95d071a2-3a3f-424f-826b-df4ad5880e61" />



---

# 📄 **13. Pagination**

`settings.py`:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": 
        "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10
}
```

Result:

```
{
  "count": 15,
  "next": "...?limit=10&offset=10",
  "results": [...]
}
```
<img width="833" height="441" alt="image" src="https://github.com/user-attachments/assets/356ca94e-b335-41ee-8fa1-d5c05812eed9" />

---

# 🔍 **14. Search API (Q-Objects)**

```python
def search(self, query):
    return self.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query)
    )
```

Example:

```
/api/search/?q=laptop
```
<img width="975" height="525" alt="image" src="https://github.com/user-attachments/assets/ae6636c7-8789-446d-94e0-1f8b75168d44" />

---

# 🌐 **15. CORS Handling (Port 8111)**

Your JS client runs on:

```
http://127.0.0.1:8111/
```

Add to settings:

```python
INSTALLED_APPS += ["corsheaders"]

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8111",
    "http://localhost:8111"
]
```

---

# 🧪 **16. JavaScript Client (8111)**

### Login

```javascript
fetch("http://127.0.0.1:8000/api/token/", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({ username, password })
})
.then(res => res.json())
.then(data => localStorage.setItem("access", data.access));
```

### Authenticated Request

```javascript
fetch("http://127.0.0.1:8000/api/products/", {
  headers: {
    "Authorization": "Bearer " + localStorage.getItem("access")
  }
})
```
<img width="975" height="346" alt="image" src="https://github.com/user-attachments/assets/e6b87944-f1b2-44c1-b874-fd8c9070a43a" />

---
