from rest_framework.permissions import BasePermission, SAFE_METHODS
from .serializers import Representation


class AnyoneWatches(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS)


class UserMakesNew(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and request.method == 'POST')


class AuthorChanges(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Representation):
            return False
        return bool(request.user.is_authenticated and request.user == obj.author)


class ModeratorChanges(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and request.user.role == 'moderator')


class AdminChanges(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and request.user.is_staff)


class SuperuserChanges(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and request.user.is_superuser)
