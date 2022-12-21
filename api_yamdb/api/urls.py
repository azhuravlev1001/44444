from .routers import router
from django.urls import path, include

api_version = "v1"

urlpatterns = [
    path(f"{api_version}/", include(router.urls)),
]
