# Django
from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAuthenticated,
)

from reviews.models import User


class AnyoneWatches(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS)


class UserMakesNew(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            super().has_permission(request, view) and request.method == 'POST'
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            super().has_object_permission(request, view, obj)
            and request.method == 'POST'
        )


class AuthorChanges(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(
            super().has_permission(request, view)
            and request.user == obj.author
        )


class ModeratorChanges(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            super().has_permission(request, view)
            and request.user.role == User.Role.MODERATOR
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            super().has_object_permission(request, view, obj)
            and request.user.role == User.Role.MODERATOR
        )


class AdminChanges(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            super().has_permission(request, view)
            and request.user.role == User.Role.ADMIN
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            super().has_object_permission(request, view, obj)
            and request.user.role == User.Role.ADMIN
        )


class SuperuserChanges(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            super().has_permission(request, view) and request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            super().has_object_permission(request, view, obj)
            and request.user.is_superuser
        )
