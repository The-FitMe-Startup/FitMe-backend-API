from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it. TODO
    """
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        # Read permissions are only allowed to the owner of the snippet.
        return obj == request.user or request.user.is_superuser

class IsSelf(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it. TODO
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are only allowed to the owner of the snippet.
        return obj == request.user

class IsAuthorOrReadAndCreateOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it. TODO
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Read permissions are only allowed to the owner of the snippet.
        return obj.author == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
