from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it. TODO
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Read permissions are only allowed to the owner of the snippet.
        return request.user and request.user.is_authenticated and (obj == request.user or request.user.is_staff)


class IsSelf(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it. TODO
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are only allowed to the owner of the snippet.
        return request.user and request.user.is_authenticated and obj == request.user


class IsAuthorOrReadAndCreateOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it. TODO
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Read permissions are only allowed to the owner of the snippet.
        return request.user and request.user.is_authenticated and obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated and request.user.is_staff


class IsAuthenticatedToCreateOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.method == "POST" and request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (request.user and request.user.is_staff)
