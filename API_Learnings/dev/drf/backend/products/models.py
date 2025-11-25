# products/models.py

from django.db import models
from django.conf import settings 
from django.db.models import Q # <-- NEW: Import Q-object for complex lookups

# Use the AUTH_USER_MODEL string reference for the foreign key.
User = settings.AUTH_USER_MODEL 

# --- 1. Custom QuerySet (for reusable filtering) ---
class ProductQuerySet(models.QuerySet):
    def is_public(self):
        """Filters the queryset to include only public products."""
        return self.filter(public=True)

    def search(self, query=None, user=None):
        """
        Performs a case-insensitive search across title and content.
        Combines public results with the user's non-public results if a user is provided.
        """
        # 1. Initialize empty queryset
        qs = self.none() 

        # 2. Base Lookup: Search across title OR content
        if query is not None:
            # Q-object creates a complex OR lookup: title contains query OR content contains query
            lookup = Q(title__icontains=query) | Q(content__icontains=query)

            # Get public products that match the lookup
            qs_public = self.is_public().filter(lookup) 
            qs = qs_public
            
            # 3. If User is Authenticated, include their non-public matching items
            if user is not None:
                # Get the user's products (public or private) that match the lookup
                qs_user = self.filter(user=user).filter(lookup)
                
                # Combine the two querysets and ensure no duplicates using .distinct()
                qs = (qs_public | qs_user).distinct()
            
        return qs # Will return a queryset, potentially empty if no query


# --- 2. Custom Manager (to inject the QuerySet) ---
class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        """Overrides default manager to return our custom QuerySet."""
        # This injects ProductQuerySet methods (like .is_public() and .search())
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query=None, user=None):
        """Proxy method for the manager to call the queryset's search method."""
        return self.get_queryset().search(query, user)


# --- 3. Product Model ---
class Product(models.Model):
    user = models.ForeignKey(
        User,
        null=True, 
        on_delete=models.SET_NULL,
    )
    
    # NEW FIELD FOR SEARCH FILTERING
    public = models.BooleanField(default=True)
    
    # NEW MANAGER: Tell the model to use our custom manager
    objects = ProductManager() 

    # Existing fields
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)

    # Existing methods
    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.8)
    
    def get_discount(self):
        return "122" 

    def __str__(self):
        return self.title