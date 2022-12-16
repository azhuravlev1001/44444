# Standard Library
from datetime import datetime as dt

# Django
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from rest_framework import serializers

from reviews.models import Genre, Title, TitleGenre, User


class AuthSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150, validators=[RegexValidator('^[\\w\\|@\\.]+$')]
    )

    def validate(self, data):
        """Валидация"""
        email = data['email']
        username = data['username']

        if username == 'me':
            raise serializers.ValidationError(
                "Can't create user with name 'me'"
            )

        query = User.objects.filter(email=email).select_related()

        if query:
            if query.first().username != username:
                raise serializers.ValidationError(
                    "This email not compare with user"
                )

        query = User.objects.filter(username=username).select_related()

        if query:
            if query.first().email != email:
                raise serializers.ValidationError(
                    "This email not compare with user"
                )

        return data


class AuthConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, validators=[RegexValidator('^[\\w\\|@\\.]+$')]
    )
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150, validators=[RegexValidator('^[\\w\\|@\\.]+$')]
    )
    last_name = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)


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
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title

    def get_rating(self, obj):
        return None

    def validate_genre(self, value):
        try:
            Genre.objects.get(genre=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Такого жанра нет в списку существующих.'
            )
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
            TitleGenre.objects.get_or_create(genre=current_genre, title=title)
        return title
