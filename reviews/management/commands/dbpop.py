import datetime
import sqlite3

import pandas
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Команда заполняет базу данных'

    def handle(self, *args, **options):
        connection = sqlite3.connect('db.sqlite3')
        data_to_load = (
            (f'{settings.BASE_DIR}/static/data/titles.csv', 'reviews_title'),
            (f'{settings.BASE_DIR}/static/data/users.csv', 'users_customuser'),
            (f'{settings.BASE_DIR}/static/data/review.csv', 'reviews_review'),
            (f'{settings.BASE_DIR}/static/data/category.csv',
                'reviews_category'),
            (f'{settings.BASE_DIR}/static/data/comments.csv',
                'reviews_comment'),
            (f'{settings.BASE_DIR}/static/data/genre_title.csv',
                'reviews_genre_title'),
            (f'{settings.BASE_DIR}/static/data/genre.csv', 'reviews_genre'),
        )

        for path, table in data_to_load:
            try:
                df = pandas.read_csv(
                    path,
                    sep=',',
                    header=0,
                )
                df.rename(
                    columns={
                        'category': 'category_id',
                        'author': 'author_id',
                    },
                    inplace=True,
                )
                df.columns
                if table == 'users_customuser':
                    new_df = df.assign(
                        password='12345555',
                        is_superuser=False,
                        is_staff=False,
                        is_active=True,
                        date_joined=datetime.datetime.now(),
                        first_name='null',
                        last_name='null',
                        bio='null'
                    )
                else:
                    new_df = df
                new_df.to_sql(
                    table,
                    connection,
                    if_exists='append',
                    index=False
                )
                print(f'Данные из файла {path} загружены')
            except Exception as error:
                print(f'Остановка с ошибкой - {error}')
            finally:
                print('Конец скрипта')
