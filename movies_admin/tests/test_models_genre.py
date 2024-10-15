from django.test import TestCase

from movies.models import Genre


class GenreModelTest(TestCase):
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

    def test_types_name(self):
        """Проверка: типы полей совпадает с ожидаемым."""
        genre = GenreModelTest.genre
        field_verboses = {
            'name': 'CharField',
            'description': 'TextField',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    genre._meta.get_field(field).get_internal_type(),
                    expected_value)

    def test_object_name_is_name_fild(self):
        """Проверка: __str__  - это строчка с содержимым task.name."""
        genre = GenreModelTest.genre
        expected_object_name = genre.name
        self.assertEqual(
            expected_object_name,
            str(genre),
            "Измените класс Genre, добавив магический метод __str__: "
            "он должен возвращать строковое представление объекта."
            "Ожидается возврат поля name"
        )

    def test_db_table(self):
        """Проверка: название таблицы БД совпадает с ожидаемым."""
        genre = GenreModelTest.genre
        expected_db_table = 'content"."genre'
        self.assertEqual(expected_db_table, genre._meta.db_table)

    def test_verbose_name_table(self):
        """Проверка: verbose_name совпадает с ожидаемым."""
        genre = GenreModelTest.genre
        self.assertRegex(str(genre._meta.verbose_name), r'[а-яА-Я]+',
                         msg="Имя таблицы должно быть на русском языке.")
        self.assertRegex(str(genre._meta.verbose_name_plural), r'[а-яА-Я]+',
                         msg="Имя таблицы должно быть на русском языке.")
