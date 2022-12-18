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
        title = Title.objects.create(**validated_data)
        for genre in genres:
            TitleGenre.objects.create(genre=genre, title=title)
        return title

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

