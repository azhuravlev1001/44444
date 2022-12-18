from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, CategoryViewSet, TitleViewSet

router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'categories/<slug:slug>/', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'genres/^[a-z0-9]+(?:-[a-z0-9]+)*$/', GenreViewSet)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'titles/(?P<titles_id>\d+)', TitleViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]