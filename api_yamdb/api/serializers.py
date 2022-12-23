# Standard Library
from datetime import datetime as dt

# Django
from django.core.validators import RegexValidator
from rest_framework import serializers

# Yamdb
from api.validators import UserEmailValidator, UserNameValidator
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    TitleGenre,
    User,
)


class AuthSignupSerializer(serializers.Serializer):
    """Класс сериализации данных регистрации нового пользователя"""

    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150, validators=[RegexValidator('^[\\w\\|@\\.]+$')]
    )

    def validate(self, data):
        """Валидация"""

        email = data['email']
        username = data['username']

        # Ограничение на api пользователя
        if username.lower() == 'me':
            raise serializers.ValidationError(
                "Нельзя создавать пользователя с именем 'me'"
            )

        # Ограничение на дубликат username
        query = User.objects.filter(email=email).select_related()
        if query:
            if query.first().username != username:
                raise serializers.ValidationError(
                    "Указанное имя уже используется"
                )

        # Ограничение на дубликат email
        query = User.objects.filter(username=username).select_related()
        if query:
            if query.first().email != email:
                raise serializers.ValidationError(
                    "Указанный email уже используется"
                )

        return data


class AuthConfirmSerializer(serializers.Serializer):
    """Класс сериализации данных подтверждения регистрации"""

    username = serializers.CharField(
        max_length=150, validators=[RegexValidator('^[\\w\\|@\\.]+$')]
    )
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализации модели User"""

    email = serializers.EmailField(
        max_length=254, validators=[UserEmailValidator()]
    )
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator('^[\\w\\|@\\.]+$'), UserNameValidator()],
    )
    last_name = serializers.CharField(max_length=150, required=False)
    first_name = serializers.CharField(max_length=150, required=False)

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

    # def get_user(self):
    #     """Возвращает текущего пользователя"""

    #     user = None
    #     request = self.context.get("request")
    #     if request and hasattr(request, "user"):
    #         user = request.user
    #     return user

    # def get_method(self):
    #     """Возвращает текущий метод"""

    #     return self.context.get("request").method

    # def validate_email(self, value):
    #     """Валидация email"""

    #     if self.get_method() == 'POST':
    #         if self.get_user().role == User.Role.ADMIN:
    #             if User.objects.filter(email=value).select_related():
    #                 raise serializers.ValidationError(
    #                     'Пользователь с таким email уже существует.'
    #                 )
    #     return value

    # def validate_username(self, value):
    #     """Валидация username"""

    #     if self.get_method() == 'POST':
    #         if self.get_user().role == User.Role.ADMIN:
    #             if User.objects.filter(username=value).select_related():
    #                 raise serializers.ValidationError(
    #                     'Пользователь с таким username уже существует.'
    #                 )
    #     return value


class GenreSerializer(serializers.ModelSerializer):
    """Сериализация жанров"""

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация категориев"""

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class CreateTitleSerializer(serializers.ModelSerializer):
    """Сериализация создания произведений"""

    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    description = serializers.CharField(required=False)

    class Meta:
        fields = '__all__'
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
    """Сериализация произведений"""

    rating = serializers.IntegerField(source='get_rating')
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fields = ('rating', 'category', 'genre')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Отзывы"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    score = serializers.ChoiceField(choices=range(1, 11))

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Комментарии"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
