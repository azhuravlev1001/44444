### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:killjoynfk/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Source/Activate
```

Установить зависимости из файла requirements.txt:

```
python -r requirements.txt
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
cd yatube_api
```

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

Для импорта базы данных из файлов CSV используйте команду import_csv

```
python manage.py import_csv --help
```