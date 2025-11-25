from rest_framework import generics
from products.models import Product
from products.serializers import ProductSerializer

class SearchListView(generics.ListAPIView):
    # This view will inherit pagination from settings.py
    
    # We set the default queryset to all products (optional, but clean)
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        # 1. Get the initial query set from the parent class (respects UserQuerySetMixin if used, etc.)
        qs = super().get_queryset(*args, **kwargs)
        
        # 2. Extract the 'q' parameter from the URL query string (?q=term)
        q = self.request.GET.get('q') 
        user = None
        
        # 3. Check for authenticated user
        if self.request.user.is_authenticated:
            user = self.request.user

        # 4. Perform Search using the custom manager method
        if q is not None:
            # Note: We call Product.objects.search() which uses the logic in models.py
            return Product.objects.search(query=q, user=user)
        
        # If no query is provided, return an empty queryset (no results)
        return Product.objects.none()