# Django
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Comment, Review, Title, User
from .serializers import ReviewSerializer, get_content, RepresentationSerializer, CommentSerializer


# class ReviewsAPIView(APIView):
#     def get(self, request, title_id):
#         queryset = Review.objects.filter(title__id=title_id)
#         content = get_content(Title, queryset, title_id, ListOfReviewsSerializer)
#         return Response(content)

#     def post(self, request, title_id):
#         review_new = Review.objects.create(
#             text=request.data['text'],
#             title=get_object_or_404(Title, id=title_id),
#             author=get_object_or_404(User, id=102),        # request.user
#             score=request.data['score']
#         )
#         return Response(ListOfReviewsSerializer(review_new).data)


# class SingleReviewViewSet(ModelViewSet):
#     serializer_class = ListOfReviewsSerializer

#     def get_queryset(self):
#         return Review.objects.filter(title__id=self.kwargs['title_id'])
        # return Review.objects.filter(pk=1)
        # return get_object_or_404(Review, pk=1)

    # def perform_create(self, serializer):
    #     title = get_object_or_404(Title, id=self.kwargs['title_id'])
    #     serializer.save(author=self.request.user, title=title)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(title__id=self.kwargs['title_id'])

    def list(self, request, title_id):
        queryset = Review.objects.filter(title__id=title_id)
        content = get_content(Title, queryset, title_id, ReviewSerializer)
        serializer = RepresentationSerializer(content)
        return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(review__id=self.kwargs['review_id'])

    def list(self, request, title_id, review_id):
        queryset = Comment.objects.filter(review__id=review_id)
        content = get_content(Review, queryset, review_id, CommentSerializer)
        serializer = RepresentationSerializer(content)
        return Response(serializer.data)

# class ReviewsViewSet(ModelViewSet):
#     serializer_class = AllReviewsSerializer
#     # permission_classes = []

#     def get_queryset(self):
#         return Review.objects.filter(title__id=self.kwargs['title_id'])

#     def perform_create(self, serializer):
#         title = get_object_or_404(Title, id=self.kwargs['title_id'])
#         serializer.save(author=self.request.user, title=title)


# class ReviewViewSet(ModelViewSet):
#     serializer_class = ReviewSerializer
#     # permission_classes = []

#     def get_queryset(self):
#         queryset = Review.objects.filter(
#             id=self.kwargs['review_id'],
#             title__id=self.kwargs['title_id']
#         )
#         return queryset

#     def perform_create(self, serializer):
#         title = get_object_or_404(Title, id=self.kwargs['title_id'])
#         serializer.save(author=self.request.user, title=title)


# class CommentViewSet(ModelViewSet):
#     serializer_class = CommentSerializer
#     # permission_classes = []

#     def get_queryset(self):
#         queryset = Comment.objects.filter(review__id=self.kwargs['review_id'])
#         return queryset

#     def perform_create(self, serializer):
#         review = get_object_or_404(Review, id=self.kwargs['review_id'])
#         serializer.save(author=self.request.user, review=review)


# class TitleViewSet(ModelViewSet):
#     serializer_class = TitleSerializer
#     # permission_classes = []
#     queryset = Title.objects.all()



