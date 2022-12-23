# Django
from rest_framework.serializers import ValidationError

# Yamdb
from reviews.models import User


class BaseContextValidator:
    """Базовй класс для реализации валиадции с использованием контекста"""

    requires_context = True
    serializer = None

    def get_user(self):
        request = self.serializer.context['request']
        return request.user

    def get_method(self):
        request = self.serializer.context['request']
        return request.method

    def validate(self, value):
        """Функция проверки"""
        return value

    def __call__(self, value, serializer):
        if not serializer:
            raise ValidationError('Нет контекста в валидции параметра.')

        self.serializer = serializer
        return self.validate(value)


class UserEmailValidator(BaseContextValidator):
    """Валидация email при POST запросе администратора"""

    def validate(self, value):
        if (
            self.get_method() == 'POST'
            and self.get_user().role == User.Role.ADMIN
            and User.objects.filter(email=value).select_related()
        ):
            raise ValidationError('Пользователь с таким email уже существует.')
        return value


class UserNameValidator(BaseContextValidator):
    """Класс для валидации username при POST запросе администратора"""

    def validate(self, value):
        if (
            self.get_method() == 'POST'
            and self.get_user().role == User.Role.ADMIN
            and User.objects.filter(username=value).select_related()
        ):
            raise ValidationError(
                'Пользователь с таким username уже существует.'
            )
        return value
