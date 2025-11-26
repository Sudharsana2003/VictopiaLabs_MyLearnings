from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import ProductViewSet

router = DefaultRouter()
router.register(r'', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]

