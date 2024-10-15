from datetime import datetime

from django.test import TestCase

from movies.models import Filmwork, Genre, Person, PersonFilmwork


class PersonFilmworkTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        # и сохраняем созданную запись в качестве переменной класса
        cls.genre = Genre.objects.create(
            name='Драма',
            description='Жанр, повествующий о серьезных, иногда печальных '
                        'событиях, но не заканчивающийся трагическим финалом.',
        )
        cls.person = Person.objects.create(
            full_name='Леонардо Вильгельм Ди Каприо'
        )

        cls.film_work = Filmwork.objects.create(
            title='Что гложет Гилберта Грэйпа',
            description='Американская драма 1993 года режиссёра Лассе '
            'Халльстрёма. Фильм является экранизацией одноимённого романа '
            'Питера Хеджеса, который также выступил автором сценария.',
            creation_date=datetime.strptime(
                'Sep 17 1993',
                '%b %d %Y').date(),
            rating=7.9,
            type='movie',
        )
        cls.film_work.genres.set([cls.genre])

        cls.person_filmwork = PersonFilmwork.objects.create(
            person=cls.person,
            film_work=cls.film_work,
            role='actor',
        )

    def test_types_name(self):
        """Проверка: типы полей совпадает с ожидаемым."""
        person_filmwork = PersonFilmworkTest.person_filmwork
        field_verboses = {
            'role': ('CharField', 'TextField'),  # Добавлен TextField в список
            'created': 'DateTimeField',
        }
        for field, expected_values in field_verboses.items():
            with self.subTest(field=field):
                field_type = person_filmwork._meta.get_field(
                    field).get_internal_type()
                self.assertIn(
                    field_type,
                    expected_values,
                    f"Тип поля '{field}' должен быть {expected_values}, "
                    f"а не '{field_type}'"
                )

    def test_db_table(self):
        """Проверка: название таблицы БД совпадает с ожидаемым."""
        person_filmwork = PersonFilmworkTest.person_filmwork
        expected_db_table = 'content"."person_film_work'
        self.assertEqual(expected_db_table, person_filmwork._meta.db_table)
