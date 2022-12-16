# Django
from django.urls import include, path
from rest_framework.routers import DefaultRouter

# Yatube
from api.views import AuthViewSet, UserViewSet

v1_router = DefaultRouter()
v1_router.register('auth', AuthViewSet, basename='auth')
v1_router.register('users', UserViewSet, basename='users')

api_version = "v1"

urlpatterns = [
    path(f"{api_version}/", include(v1_router.urls)),
]
