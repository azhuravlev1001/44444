from .routers import router
from django.urls import include, path

app_name = 'reviews'

urlpatterns = [
    path('v1/', include(router.urls)),
]
