# products/mixins.py

from rest_framework import permissions

# --- Permissions Mixin ---
class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    """
    Custom permission check:
    - Allows GET/HEAD/OPTIONS (safe methods) if the user is authenticated.
    - Allows POST/PUT/DELETE if the user is in the 'staff_editor' group 
      AND has the Django model permissions (add, change, delete).
    """
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        # Allow Safe Methods (GET, HEAD, OPTIONS) if the user is authenticated
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        
        # Check if user is staff (is_staff=True)
        if request.user.is_staff:
            # Check if user is in the 'staff_editor' group
            # Note: This is a placeholder for your custom group logic.
            # permissions.DjangoModelPermissions handles the actual model permission check.
            return super().has_permission(request, view)

        return False


class StaffEditorPermissionMixin:
    """
    Mixin to apply the StaffEditorPermission and required authentication.
    """
    authentication_classes = [permissions.IsAuthenticated] 
    permission_classes = [IsStaffEditorPermission] 


# --- Queryset Mixin ---
class UserQuerySetMixin:
    """
    Mixin to filter the queryset based on the requesting user.
    - If user is staff and 'allow_staff_view' is True, returns all products.
    - Otherwise, filters products to only include those owned by the user.
    """
    # The ForeignKey field on the Product model pointing to the User model.
    user_field = 'user' 
    
    # Setting this to True in a View will allow staff users to see ALL products.
    # The default is False, meaning staff users will also only see their own.
    # We will set this to True in the List views in views.py.
    allow_staff_view = False 

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        
        # 1. Staff override check
        # If the view sets allow_staff_view=True AND the user is staff, return the full queryset.
        if self.allow_staff_view and user.is_staff:
            return super().get_queryset(*args, **kwargs)

        # 2. Queryset filtering for the current user
        # Filter the queryset to only include products where the user_field (e.g., 'user') 
        # matches the authenticated user.
        lookup_data = {self.user_field: user}
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(**lookup_data)