# Standard Library
import csv
from os.path import exists

# Django
from django.core.management.base import BaseCommand, CommandError

from reviews.models import User


class Command(BaseCommand):
    help = 'Import csv files to table of DB'

    TABLES = {
        'User': User,
    }

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', nargs='+', type=str, required=True)
        parser.add_argument(
            '-t',
            '--table',
            choices=self.TABLES.keys(),
            type=str,
            required=True,
        )

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

        model = self.TABLES[table]
        with open(file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            headers = []
            for row in reader:
                headers = row
                break

            for row in reader:
                data = {}
                for position, header in enumerate(headers):
                    data[header] = row[position]

                model.objects.get_or_create(**data)

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully load table: {str(table)}, from file: {file}'
                )
            )

    def handle(self, *args, **options):
        files = options['file']
        table = options['table']

        for file in files:
            self.import_table(file, table)
