from rest_framework.permissions import BasePermission, SAFE_METHODS

def is_site_admin(user):
    return bool(user and user.is_authenticated and (user.is_staff or user.is_superuser))

class NotePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return is_site_admin(request.user)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.status == 'published' or is_site_admin(request.user)
        return is_site_admin(request.user)
