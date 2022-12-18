from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from reviews.models import Title, Category, Genre
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from .permissions import ReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    # permission_classes = (permissions.IsAdminUser,)
    #
    # def get_permissions(self):
    #     if self.action == 'list':
    #         return (ReadOnly(),)
    #     return super().get_permissions()

    # def get_post_id(self):
    #     """Возвращает id поста из запроса"""
    #     KEY_POST_ID = "post_id"
    #     if KEY_POST_ID not in self.kwargs:
    #         raise Exception(f"В запросе не указан {KEY_POST_ID}")
    #     return self.kwargs.get(KEY_POST_ID)
    #
    # def get_post_object(self) -> Post:
    #     """Возвращает связанный объект поста"""
    #     return get_object_or_404(Post, pk=self.get_post_id())

    # def get_slug(self):
    #     if 'slug' not in self.kwargs:
    #         raise Exception('В запросе не указан slug')
    #     return self.kwargs.get('slug')
    #
    # def get_post_object(self, request):
    #
    #     return get_object_or_404(Post, pk=self.get_post_id())

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    # permission_classes = (permissions.IsAdminUser,)
    #
    # def get_permissions(self):
    #     if self.action == 'list':
    #         return (ReadOnly(),)
    #     return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (permissions.IsAdminUser,)
    #
    # def get_permissions(self):
    #     if self.action in ['list', 'retrive']:
    #         return (ReadOnly(),)
    #     return super().get_permissions()
