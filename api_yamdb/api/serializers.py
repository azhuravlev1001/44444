from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from datetime import datetime as dt

from reviews.models import Title, Genre, TitleGenre


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, required=False)
    category = GenreSerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        return None

    def validate_genre(self, value):
        try:
            Genre.objects.get(genre=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Такого жанра нет в списку существующих.')
        return value

    def validate_year(self, value):
        year = dt.date().today().year
        if value > year:
            raise serializers.ValidationError('Проверьте указанную дату.')
        return value

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            TitleGenre.objects.get_or_create(
                genre=current_genre,
                title=title
            )
        return title