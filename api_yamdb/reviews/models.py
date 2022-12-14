# Django
from django.contrib.auth.models import AbstractUser
from django.db import models


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
