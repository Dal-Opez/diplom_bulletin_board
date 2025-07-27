from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменение только владельцу объекта.
    Чтение разрешено всем.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает создание/изменение только администраторам.
    Чтение разрешено всем.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and (request.user.role == "ADMIN" or request.user.is_staff)


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешает изменение владельцу или администратору.
    Чтение разрешено всем.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user) or (
            request.user and (request.user.role == "ADMIN" or request.user.is_staff)
        )
