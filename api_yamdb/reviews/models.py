# Django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import (
    CASCADE,
    Avg,
    DateTimeField,
    ForeignKey,
    Model,
    PositiveSmallIntegerField,
    TextField,
)

STR_LENGTH = 15


class User(AbstractUser):
    """Кастомизированная модель пользователя"""

    class Role(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    role = models.TextField(
        choices=Role.choices,
        default=Role.USER,
        blank=True,
        verbose_name='Роль пользователя',
        help_text='Укажите роль пользователя',
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография пользователя',
        help_text='Заполните биографию пользователя',
    )


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Title(models.Model):
    """Метод для определения рейтинга get_rating"""
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='titles'
    )

    def get_rating(self):
        rating = Review.objects.filter(title__id=self.id).aggregate(Avg('score'))['score__avg']
        return round(rating)

    def __str__(self):
        return self.name


class Review(Model):
    """Модель отзывов"""
    text = TextField(
        verbose_name='Текст отзыва', help_text='Введите текст отзыва'
    )
    title = ForeignKey(
        Title,
        verbose_name='Произведение',
        help_text='Произведение, на которое оставляем отзыв',
        on_delete=CASCADE,
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Автор отзыва',
        help_text='Автор отзыва',
    )
    score = PositiveSmallIntegerField(
        verbose_name='Оценка отзыва',
        help_text='Оценка отзыва, число от 1 до 10',
    )
    pub_date = DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True,
        help_text='Дата публикации отзыва (ставится автоматически)',
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:STR_LENGTH]


class Comment(Model):
    """Модель комментариев"""
    review = ForeignKey(
        Review,
        on_delete=CASCADE,
        verbose_name='Комментарий',
        help_text='Комментарий к отзыву',
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Автор комментария',
        help_text='Автор комментария',
    )
    text = TextField(
        verbose_name='Текст комментария', help_text='Введите текст комментария'
    )
    pub_date = DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
        help_text='Дата комментария (ставится автоматически)',
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:STR_LENGTH]


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='title'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='genre'
    )
