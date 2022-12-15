Модели api_yamdb\reviews\models.py, Сериалайзеры api_yamdb\reviews\serializers.py, Вьюсеты api_yamdb\reviews\views.py - для Отзывы (`Review`), Комментарии (`Comment`) 

Вьюсет `TitleViewSet` - демо вариант

Метод `get_rating` в модели `Title` - настроен

`TitleSerializer` - демо вариант, обеспечивает отображение рейтинга

Эндпоинты api_yamdb\reviews\urls.py, роутеры для `TitleViewSet` `ReviewViewSet` `CommentViewSet` api_yamdb\reviews\routers.py - настроены.

Нужно доработать сериалайзеры `ReviewSerializer` `CommentSerializer` согласно заданию. 