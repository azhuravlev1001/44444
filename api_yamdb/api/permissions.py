from rest_framework.permissions import (BasePermission,
                                        IsAuthenticated,
                                        SAFE_METHODS)

from reviews.models import User


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAdmin(IsAuthenticated):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.user.is_superuser or request.user.role == User.Role.ADMIN
        )


class IsModerator(IsAuthenticated):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.user.is_superuser
            or request.user.role == User.Role.MODERATOR
        )


class AnyoneWatches(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS)


class UserMakesNew(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and request.method == 'POST'
        )


class AuthorChanges(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and request.user == obj.author
        )


class ModeratorChanges(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and request.user.role == 'moderator'
        )


class AdminChanges(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and request.user.is_staff)


class SuperuserChanges(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and request.user.is_superuser
        )
