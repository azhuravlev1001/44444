from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from datetime import datetime as dt

from reviews.models import Title, Genre, Category, TitleGenre


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class CreateTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    description = serializers.CharField(required=False)

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')
        model = Title

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        categories = validated_data.pop('category')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            TitleGenre.objects.create(
                genre=current_genre,
                title=title
            )
        for category in categories:
            Category.objects.create(**category)
        return title

    def validate_genre(self, value):
        try:
            Genre.objects.get(genre=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Такого жанра нет в списку существующих.')
        return value

    def validate_year(self, value):
        year = dt.now().year
        if value > year:
            raise serializers.ValidationError('Проверьте указанную дату.')
        return value


class GetTitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title
        read_only_fields = ('rating', 'category', 'genre')

    def get_rating(self, obj):
        return None

