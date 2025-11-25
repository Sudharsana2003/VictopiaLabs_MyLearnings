# products/views.py

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly 

from .models import Product
from .serializers import ProductSerializer
# Import the necessary mixins
from .mixins import StaffEditorPermissionMixin, UserQuerySetMixin


# 1. ProductListCreateAPIView: Applies filtering and assigns user on create
class ProductListCreateAPIView(
    UserQuerySetMixin, 
    generics.ListCreateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # FIX: Allow staff users (sri, kala) to see the full list of products
    allow_staff_view = True 

    def perform_create(self, serializer):
        # Assign the user field based on the authenticated request user.
        serializer.save(user=self.request.user)

product_list_create_view = ProductListCreateAPIView.as_view()


# 2. ProductDetailAPIView: Applies filtering
class ProductDetailAPIView(UserQuerySetMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Allow staff users to see the detail of any product
    allow_staff_view = True 

product_detail_view = ProductDetailAPIView.as_view()


# 3. ProductRetrieveUpdateAPIView: Applies filtering and Staff permissions
class ProductRetrieveUpdateAPIView(
    StaffEditorPermissionMixin, 
    UserQuerySetMixin, 
    RetrieveUpdateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    
    # We will rely on Object-Level Permissions (to be added later) for who can update/delete.
    # For now, this allows staff editors to access the item if they own it or if permissions allow.
    allow_staff_view = True 

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            instance.save()

product_update_view = ProductRetrieveUpdateAPIView.as_view()


# 4. ProductDeleteAPIView: Applies filtering and Staff permissions
class ProductDeleteAPIView(
    StaffEditorPermissionMixin, 
    UserQuerySetMixin, 
    generics.DestroyAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    
    allow_staff_view = True 

product_delete_view = ProductDeleteAPIView.as_view()


# 5. ProductMixinView: Applies filtering and Staff permissions
class ProductMixinView(
    StaffEditorPermissionMixin, 
    UserQuerySetMixin, 
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    allow_staff_view = True 

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user) 
        return Response(serializer.data, status=201)

product_mixin_view = ProductMixinView.as_view()


@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    # This is a function-based view and does NOT use the mixins.
    if request.method == "GET":
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj).data
            return Response(data)
        qs = Product.objects.all()
        data = ProductSerializer(qs, many=True).data
        return Response(data)

    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                serializer.save(user=request.user)
            else:
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)