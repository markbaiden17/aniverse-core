from rest_framework.permissions import BasePermission, SAFE_METHODS

# -----------------------------------------------------------------------------
# Object-Level Permission: Owner or Read-Only
# -----------------------------------------------------------------------------

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to ensure that only the creator of a review
    can edit or delete it, while allowing public read access.
    """
    # Custom error message returned when a permission check fails
    message = "You do not have permission to modify or delete another user's review."

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform the requested action
        on a specific Review instance.
        """
        # Allow GET, HEAD, or OPTIONS requests (SAFE_METHODS) for any user
        if request.method in SAFE_METHODS:
            return True
            
        # Write permissions (POST, PUT, PATCH, DELETE) only granted to the owner
        return obj.user == request.user