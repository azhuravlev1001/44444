# Django
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import CharField, IntegerField, ListField, ChoiceField, ModelSerializer, Serializer
from django.shortcuts import get_object_or_404

from .models import Comment, Review, Title, User


class Representation:
    """Класс для данных "верхнего уровня" """
    def __init__(self, count, next, previous, results):
        self.count = count
        self.next = next
        self.previous = previous
        self.results = results


class RepresentationSerializer(Serializer):
    """Сериалайзер для данных "верхнего уровня" """
    count = IntegerField()
    next = CharField()
    previous = CharField()
    results = ListField()


def get_serial(Upmodel, queryset, lookup, Serializer):
    """Типовая функция для сериализации данных "верхнего уровня" """
    content = Representation(
        count=queryset.count(),
        next=str(get_object_or_404(Upmodel, pk=int(lookup) + 1)),
        previous=str(get_object_or_404(Upmodel, pk=int(lookup) - 1)),
        results=Serializer(queryset, many=True).data
    )
    return RepresentationSerializer(content)


class ReviewSerializer(ModelSerializer):
    """Сериалайзер для модели Отзывы"""
    author = SlugRelatedField(read_only=True, slug_field='username')
    score = ChoiceField(choices=range(1, 11))

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(ModelSerializer):
    """Сериалайзер для модели Комментарии"""
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


# class TitleSerializer(ModelSerializer):
#     rating = IntegerField(source='get_rating', read_only=True)

#     class Meta:
#         model = Title
#         fields = ('name', 'year', 'description', 'genre', 'category', 'rating')
