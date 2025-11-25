from rest_framework.permissions import BasePermission

class IsStaffEditorPermission(BasePermission):
    """
    Staff users can access endpoints based on:
    1. ProductGroup membership
    2. Individual permissions
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if user.is_staff:
            # Use user.has_perm (automatically checks group + individual perms)
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                return user.has_perm('products.view_product')
            elif request.method == 'POST':
                return user.has_perm('products.add_product')
            elif request.method in ['PUT', 'PATCH']:
                return user.has_perm('products.change_product')
            elif request.method == 'DELETE':
                return user.has_perm('products.delete_product')

        return False
