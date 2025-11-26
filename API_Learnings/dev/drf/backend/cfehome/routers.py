# backend/cfehome/routers.py
from rest_framework.routers import DefaultRouter
from products.viewsets import ProductViewSet, ProductReadOnlyGenericViewSet

router = DefaultRouter()
# register full CRUD at /api/v2/products/
router.register(r'products', ProductViewSet, basename='products')

# optional: register the read-only variant at a different prefix
# router.register(r'products-readonly', ProductReadOnlyGenericViewSet, basename='products-readonly')

# expose urls so they can be included from root urls
urlpatterns = router.urls
