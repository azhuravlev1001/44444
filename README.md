# Краткое описание финального проекта по API YaMDb

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

# Используемые технологии и библиотеки:
- python 3.7.0
- requests 2.26.0
- Django 3.2
- djangorestframework 3.12.4
- PyJWT 2.1.0
- pytest 6.2.4
- pytest-django 4.4.0
- pytest-pythonpath 0.7.3
- djangorestframework-simplejwt 5.2.2
- django-filter 22.1

# Установка и настройки
Клонировать репозитория
```
git@github.com:azhuravlev1001/api_yamdb.git
```

## Cоздание и активация виртуального окружения:

```
cd api_yamdb
```

```
python -m venv env
```

```
source venv/Source/Activate
```

## Установка зависимостей из файла requirements.txt:

```
python -r requirements.txt
```

```
pip install -r requirements.txt
```

## Выполнение миграций:

```
cd api_yamdb
```

```
python manage.py migrate
```

## Заполнение базы данных из CSV:

```
python manage.py import_csv -f [FILE ...] -t [User, Category, Genre, Title, Review, Comment, TitleGenre]
```
## Запуск тестов:

```
cd ..
```

```
pytest
```

## Запуск проекта:

```
cd api_yamdb
```

```
python manage.py runserver
```


# Документация:

Документация по API доступна по следующему адресу (необходимо запустить сервер):
http://172.0.0.1:8000/redoc/

# Пример запроса к API:

GET-запрос: http://172.0.0.1:8000/api/v1/titles/

Пример ответа:
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 6,
            "rating": 8,
            "genre": [
                {
                    "name": "Вестерн",
                    "slug": "western"
                }
            ],
            "category": {
                "name": "Фильм",
                "slug": "movie"
            },
            "name": "Хороший, плохой, злой",
            "year": 1966,
            "description": ""
        }
     ]
}
```

# Разработчики:
- Глухов Павел
- Головин Денис
- Журавлев Алексей

