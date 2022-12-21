# Django
from django.urls import include, path

# Yamdb
from api.routers import router

api_version = "v1"

urlpatterns = [
    path(f"{api_version}/", include(router.urls)),
]
