from datetime import datetime

from django.test import TestCase

from movies.models import Filmwork, Genre, GenreFilmwork, Person


class GenreFilmworkTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовые записи в БД
        # и сохраняем созданные записи в качестве переменных класса
        cls.genre = Genre.objects.create(
            name='Комедия', description='Жанр художественного произведения, '
            'характеризующийся юмористическим или сатирическим подходами.', )
        cls.person = Person.objects.create(
            full_name='Роуэн Себастьян Аткинсон'
        )

        cls.film_work = Filmwork.objects.create(
            title='Мистер Бин на отдыхе',
            description='Британо-франко-американо-немецкая комедия 2007 года '
                        'режиссёра Стива Бенделака.',
            creation_date=datetime.strptime(
                'Mar 29 2007',
                '%b %d %Y').date(),
            rating=6.9,
            type='movie',
        )
        cls.genre_film_work = GenreFilmwork.objects.create(
            genre=cls.genre,
            film_work=cls.film_work,
        )

    def test_types_name(self):
        """Проверка: типы полей совпадает с ожидаемым."""
        genre_film_work = GenreFilmworkTest.genre_film_work
        field_verboses = {
            'created': 'DateTimeField',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(genre_film_work._meta.get_field(
                    field).get_internal_type(), expected_value)

    def test_db_table(self):
        """Проверка: название таблицы БД совпадает с ожидаемым."""
        genre_film_work = GenreFilmworkTest.genre_film_work
        expected_db_table = 'content"."genre_film_work'
        self.assertEqual(expected_db_table, genre_film_work._meta.db_table)
