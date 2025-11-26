# backend/products/viewsets.py
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication

from .models import Product
from .serializers import ProductSerializer
from .mixins import StaffEditorPermissionMixin

# Full CRUD viewset (ModelViewSet)
class ProductViewSet(StaffEditorPermissionMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]   # optional if you rely on project defaults
    lookup_field = "pk"

# Generic viewset supporting only list + retrieve (example from video)
class ProductReadOnlyGenericViewSet(
    StaffEditorPermissionMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    lookup_field = "pk"
