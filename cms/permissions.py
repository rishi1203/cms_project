from rest_framework.permissions import BasePermission

class IsAdminOrAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.role == 'author'

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.role == 'admin'
