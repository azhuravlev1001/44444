from rest_framework import serializers
from reviews.models import User
from rest_framework import status


class UserValidator:
    def __init__(self, value):
        self.value = value

    def __call__(self, value):
        if self.get_method() == 'POST' and self.get_user().role == User.Role.ADMIN:
            if User.objects.filter(email=value).select_related():
                raise serializers.ValidationError(
                    status_code=status.HTTP_400_BAD_REQUEST
                    # 'Пользователь с таким email уже существует.'
                )
            elif User.objects.filter(username=value).select_related():
                raise serializers.ValidationError(
                    'Пользователь с таким username уже существует.'
                )
        return value

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
