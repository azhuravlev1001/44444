# Django
from rest_framework.permissions import IsAuthenticated

from reviews.models import User


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
