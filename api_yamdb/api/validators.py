# Django
from rest_framework.serializers import ValidationError

# Yamdb
from reviews.models import User


class UserEmailValidator:
    """Валидация email при POST запросе администратора"""

    def __call__(self, value):
        if User.objects.filter(email=value).select_related():
            raise ValidationError('Пользователь с таким email уже существует.')
        return value


class UserNameValidator:
    """Класс для валидации username при POST запросе администратора"""

    def __call__(self, value):
        if User.objects.filter(username=value).select_related():
            raise ValidationError(
                'Пользователь с таким username уже существует.'
            )
        return value
