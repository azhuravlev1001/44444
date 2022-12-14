from django.db import models
from django.contrib.auth.models import AbstractUser


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
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='title')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genre')
