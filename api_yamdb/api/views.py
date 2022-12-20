# Django
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import (status, viewsets, mixins,
                            permissions, filters)
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend

from api.permissions import IsAdmin, ReadOnly
from reviews.models import Category, Genre, Title, User, Comment, Review

from api.permissions import (
    IsAdmin,
    AnyoneWatches,
    UserMakesNew,
    AdminChanges,
    AuthorChanges,
    ModeratorChanges,
    SuperuserChanges
)
from .serializers import (
    AuthConfirmSerializer,
    AuthSignupSerializer,
    CategorySerializer,
    GenreSerializer,
    CreateTitleSerializer,
    GetTitleSerializer,
    UserSerializer,
    ReviewSerializer,
    CommentSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    http_method_names = ['get', 'post', 'patch', 'list', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            data = request.data.copy()
            # запрещено менять роль
            data['role'] = request.user.role
            serializer = self.get_serializer(
                request.user, data=data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(self.get_serializer(request.user).data)


class AuthViewSet(viewsets.ViewSet):
    permission_classes = []
    authentication_classes = []

    @action(detail=False, methods=['post'], url_path='signup')
    def signup(self, request):
        serializer = AuthSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, ok = User.objects.get_or_create(**serializer.validated_data)

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            'Код подтвержения регистрации пользователя',
            confirmation_code,
            settings.EMAIL_HOST_USER,
            [serializer.validated_data['email']],
            fail_silently=False,
        )
        return Response(serializer.validated_data)

    @action(detail=False, methods=['post'], url_path='token')
    def token(self, request):
        serializer = AuthConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        confirmation_code = serializer.validated_data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)})
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug',
                       'genre__slug',
                       'name',
                       'year')

    # def get_permissions(self):
    #     if self.action in ['put', 'patch', 'delete', 'create']:
    #         return [IsAdminOrSuperUser]
    #     return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return CreateTitleSerializer
        return GetTitleSerializer


class ReviewViewSet(ModelViewSet):
    """Вьюсет для модели Отзывы"""
    serializer_class = ReviewSerializer
    permission_classes = [
        AnyoneWatches
        | UserMakesNew
        | AdminChanges
        | AuthorChanges
        | ModeratorChanges
        | SuperuserChanges
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Review.objects.filter(title__id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        user = self.request.user
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        if Review.objects.filter(author=user, title=title):
            raise ValidationError(
                'Ваш отзыв на это произведение уже есть'
            )
        serializer.save(author=user, title=title)


class CommentViewSet(ModelViewSet):
    """Вьюсет для модели Комментарии"""
    serializer_class = CommentSerializer
    permission_classes = [
        AnyoneWatches
        | UserMakesNew
        | AdminChanges
        | AuthorChanges
        | ModeratorChanges
        | SuperuserChanges
    ]

    def get_queryset(self):
        return Comment.objects.filter(
            review__title__id=self.kwargs['title_id']
        ).filter(
            review__id=self.kwargs['review_id']
        )

    def perform_create(self, serializer):
        user = self.request.user
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=user, review=review)
