from rest_framework.routers import DefaultRouter
from .views import (
    GenreViewSet, CategoryViewSet, TitleViewSet,
    ReviewViewSet, CommentViewSet, AuthViewSet, UserViewSet
)

router = DefaultRouter()

router.register('auth', AuthViewSet, basename='auth')
router.register('users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(r'titles', TitleViewSet)
router.register(r'genres/^[a-z0-9]+(?:-[a-z0-9]+)*$/', GenreViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'categories/<slug:slug>/', CategoryViewSet)
router.register(r'categories', CategoryViewSet)
