from rest_framework import permissions
from reviews.models import User


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdmin(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.user.is_superuser or request.user.role == User.Role.ADMIN
        )


class IsModerator(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.user.is_superuser
            or request.user.role == User.Role.MODERATOR
        )
