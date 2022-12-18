from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Comment, Review, Title, User
from .serializers import ReviewSerializer, get_serial, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(title__id=self.kwargs['title_id'])

    def list(self, request, title_id):
        serializer = get_serial(Title, self.get_queryset(), title_id, ReviewSerializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user                          # get_object_or_404(User, pk=101)
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        if Review.objects.filter(author=user, title=title):
            raise ValidationError(
                'Ваш отзыв на это произведение уже есть'
            )
        serializer.save(author=user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(review__title__id=self.kwargs['title_id']).filter(review__id=self.kwargs['review_id'])

    def list(self, request, title_id, review_id):
        serializer = get_serial(Review, self.get_queryset(), review_id, CommentSerializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = get_object_or_404(User, pk=101)                        # self.request.user  
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=user, review=review)


# class TitleViewSet(ModelViewSet):
#     serializer_class = TitleSerializer
#     permission_classes = []
#     queryset = Title.objects.all()
