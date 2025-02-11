from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)
    

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_manager)


class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_manager or request.user.is_admin))

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_admin or request.method in SAFE_METHODS))
