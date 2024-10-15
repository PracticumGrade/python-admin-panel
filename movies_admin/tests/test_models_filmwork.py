from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase

from movies.models import Filmwork, Genre, Person


class FilmworkTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        # и сохраняем созданную запись в качестве переменной класса
        cls.genre = Genre.objects.create(
            name='Драма',
            description='Жанр, повествующий о серьезных, иногда печальных '
                        'событиях, но не заканчивающийся трагическим финалом',
        )
        cls.person = Person.objects.create(
            full_name='Леонардо Вильгельм Ди Каприо'
        )

        cls.film_work = Filmwork.objects.create(
            title='Что гложет Гилберта Грэйпа',
            description='Американская драма 1993 года режиссёра Лассе '
                        'Халльстрёма. Фильм является экранизацией '
                        'одноимённого романа Питера Хеджеса, который также '
                        'выступил автором сценария.',
            creation_date=datetime.strptime(
                'Sep 17 1993', '%b %d %Y'
            ).date(),
            rating=7.9,
            type='movie',
        )

    def test_verbose_name(self):
        """Проверка: verbose_name в полях совпадает с ожидаемым."""
        film_work = FilmworkTest.film_work
        field_verboses = {
            'title': 'Название',
            'description': 'Описание',
            'creation_date': 'Дата премьеры',
            'rating': 'Рейтинг',
            'type': 'Тип',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertRegex(
                    str(film_work._meta.get_field(field).verbose_name),
                    r'[а-яА-Я]+',
                    msg=f"verbose_name поля '{field}' "
                        f"должно быть на русском языке.")

    def test_types_name(self):
        """Проверка: Типы полей совпадает с ожидаемым."""
        film_work = FilmworkTest.film_work
        field_verboses = {
            'title': 'CharField',
            'description': 'TextField',
            'creation_date': 'DateField',
            'rating': 'FloatField',
            'type': 'CharField',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    film_work._meta.get_field(field).get_internal_type(),
                    expected_value
                )

    def test_object_name_is_full_name_fild(self):
        """Проверка: str - это строчка с содержимым film_work.title."""
        film_work = FilmworkTest.film_work
        expected_object_name = film_work.title
        self.assertEqual(expected_object_name, str(film_work))

    def test_db_table(self):
        """Проверка: Название таблицы БД совпадает с ожидаемым."""
        film_work = FilmworkTest.film_work
        expected_db_table = 'content"."film_work'
        self.assertEqual(expected_db_table, film_work._meta.db_table)

    def test_verbose_name_table(self):
        """Проверка: verbose_name совпадает с ожидаемым."""
        film_work = FilmworkTest.film_work
        self.assertRegex(str(film_work._meta.verbose_name),
                         r'[а-яА-Я]+',
                         msg="Имя таблицы должно быть на русском языке.")
        self.assertRegex(str(film_work._meta.verbose_name_plural),
                         r'[а-яА-Я]+',
                         msg="Имя таблицы должно быть на русском языке.")

    def test_rating_validators_less_than_0(self):
        """Проверка: валидатор поля rating, рейтинг должен быть больше 0."""
        film_work = Filmwork.objects.create(
            title='Что же гложет Гилберта Грэйпа.',
            description='Американская драма 1993 года режиссёра Лассе '
                        'Халльстрёма. Фильм является экранизацией '
                        'одноимённого романа Питера Хеджеса, который также '
                        'выступил автором сценария.',
            creation_date=datetime.strptime(
                'Sep 17 1993', '%b %d %Y'
            ).date(),
            rating=-0.00001,
            type='movie',
        )
        self.assertRaises(ValidationError, film_work.full_clean)

    def test_rating_validators_greater_than_100(self):
        """Проверка, что валидатор поля rating ограничивает значение до 100."""
        film_work = Filmwork.objects.create(
            title='Что же все же гложет Гилберта Грэйпа',
            description='Американская драма 1993 года режиссёра Лассе '
                        'Халльстрёма. Фильм является экранизацией '
                        'одноимённого романа Питера Хеджеса, который также '
                        'выступил автором сценария.',
            creation_date=datetime.strptime(
                'Sep 17 1993', '%b %d %Y'
            ).date(),
            rating=100.00001,
            type='movie',
        )
        self.assertRaises(ValidationError, film_work.full_clean)

    def test_many_to_many_fields(self):
        """Проверка: наличие ManyToManyField."""
        self.assertTrue(
            hasattr(Filmwork, 'genres'),
            "Должна быть описана ManyToMany связь с таблицей Genres \n"
            " genres = models.ManyToManyField(...)  "
        )
        self.assertTrue(
            hasattr(Filmwork, 'persons'),
            "Должна быть описана ManyToMany связь с таблицей Person \n"
            " persons = models.ManyToManyField(...)  "
        )

        # Проверка типа поля
        self.assertIsInstance(
            Filmwork._meta.get_field('genres'), models.ManyToManyField
        )
        self.assertIsInstance(
            Filmwork._meta.get_field('persons'), models.ManyToManyField
        )

        # Проверка подключения модели
        self.assertEqual(
            Filmwork._meta.get_field('genres').related_model, Genre
        )
        self.assertEqual(
            Filmwork._meta.get_field('persons').related_model, Person
        )
