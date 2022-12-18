# Django
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import CharField, IntegerField, ListField, ChoiceField, ModelSerializer, Serializer
from django.shortcuts import get_object_or_404

from .models import Comment, Review, Title


# class ReviewSerializer(ModelSerializer):
#     author = SlugRelatedField(read_only=True, slug_field='username')
#     score = ChoiceField(choices=range(1, 11))
#     text = CharField(max_length=500)

#     def validate(self, data):
#         user = self.context['request'].user
#         title = data['title']
#         if Review.objects.filter(author=user, title=title):
#             raise ValidationError(
#                 'Отзыв на это произведение уже есть'
#             )
#         return data

#     class Meta:
#         model = Review
#         fields = ('id', 'text', 'author', 'score', 'pub_date')


class Representation:
    def __init__(self, count, next, previous, results):
        self.count = count
        self.next = next
        self.previous = previous
        self.results = results


class RepresentationSerializer(Serializer):
    count = IntegerField()
    next = CharField()
    previous = CharField()
    results = ListField()


def get_content(Upmodel, queryset, lookup, Serializer):
    content = Representation(
        count=queryset.count(),
        next=str(get_object_or_404(Upmodel, pk=int(lookup) + 1)),
        previous=str(get_object_or_404(Upmodel, pk=int(lookup) - 1)),
        results=Serializer(queryset, many=True).data
    )
    return content


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')








# class ReviewSerializer(Serializer):
#     # results = ListOfReviewsSerializer()
#     results = IntegerField(source='get_results')


# class CommentSerializer(ModelSerializer):
#     author = SlugRelatedField(read_only=True, slug_field='username')
#     text = CharField(max_length=500)

#     class Meta:
#         model = Comment
#         fields = '__all__'


# class TitleSerializer(ModelSerializer):
#     rating = IntegerField(source='get_rating', read_only=True)

#     class Meta:
#         model = Title
#         fields = ('name', 'year', 'description', 'genre', 'category', 'rating')
