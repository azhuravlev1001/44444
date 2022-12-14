from .models_alex import Comment, Review, Title
from rest_framework.viewsets import ModelViewSet
from .serializers_alex import CommentSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404


# http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = []

    def get_queryset(self):
        queryset = Review.objects.filter(title__id=self.kwargs['title_id'])
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


# http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = []

    def get_queryset(self):
        queryset = Comment.objects.filter(review__id=self.kwargs['review_id'])
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
