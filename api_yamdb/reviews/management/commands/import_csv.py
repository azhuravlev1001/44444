# Standard Library
import csv
from os.path import exists

# Django
from django.core.management.base import BaseCommand, CommandError

# Yamdb
from reviews import models


class Command(BaseCommand):
    help = 'Import csv files to table of DB'

    MODELS = {
        'User': models.User,
        'Category': models.Category,
        'Genre': models.Genre,
        'Title': models.Title,
        'Review': models.Review,
        'Comment': models.Comment,
        'TitleGenre': models.TitleGenre,
    }

    HEADERS = {
        'author': models.User,
        'category': models.Category,
    }

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', nargs='+', type=str, required=True)
        parser.add_argument(
            '-t',
            '--table',
            choices=self.MODELS.keys(),
            type=str,
            required=True,
        )

    def import_model(self, reader, model):
        """Загружает данные из csv reader в БД

        :param reader: ридер
        :param model: модель django
        """

        headers = []
        for row in reader:
            headers = row
            break

        for row in reader:
            data = {}
            try:
                for position, header in enumerate(headers):
                    if header in self.HEADERS:
                        data[header] = self.HEADERS[header].objects.get(
                            pk=row[position]
                        )
                    else:
                        data[header] = row[position]

                model.objects.get_or_create(**data)

                self.stdout.write(self.style.NOTICE(f'Load note: {data}'))
            except Exception as what:
                self.stdout.write(
                    self.style.ERROR(f'Error to load note: {what}')
                )

        self.style.SUCCESS('Successfully load table')

    def import_table(self, file, table):
        """Загружает данные csv в БД

        :param file: путь до файла
        :type file: str
        :param table: название таблицы
        :type table: str
        :raises CommandError: вызывается исключение,
        когда не удалось найти файл
        """

        if not exists(file):
            raise CommandError(f'Can\'t find file: {file}')

        model = self.MODELS[table]
        with open(file, encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            self.import_model(reader, model)

    def handle(self, *args, **options):
        files = options['file']
        table = options['table']

        for file in files:
            self.import_table(file, table)
