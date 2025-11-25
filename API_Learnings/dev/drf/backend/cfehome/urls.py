# project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Import the views provided by simplejwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

def root_view(request):
    return JsonResponse({"status": "ok", "message": "API Root"})

urlpatterns = [
    # Root
    path("", root_view, name="root"),

    # Admin
    path("admin/", admin.site.urls),

    # API main entry (old version)
    path("api/", include("api.urls")),

    # Products API v1
    path("api/products/", include("products.urls")),

    # API v2 using viewsets & router
    path("api/v2/", include("cfehome.routers")),

    # Search API
    path('api/search/', include('search.urls')),

    # JWT Authentication 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]