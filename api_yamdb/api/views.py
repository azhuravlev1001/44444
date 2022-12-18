from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework import mixins
from reviews.models import Title, Category, Genre
from .serializers import CreateTitleSerializer, GetTitleSerializer, GenreSerializer, CategorySerializer
from .permissions import ReadOnly


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
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


class GenreViewSet(ListCreateDestroyViewSet):
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
    # permission_classes = (permissions.IsAdminUser,)
    #
    # def get_permissions(self):
    #     if self.action in ['list', 'retrive']:
    #         return (ReadOnly(),)
    #     return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return CreateTitleSerializer
        return GetTitleSerializer