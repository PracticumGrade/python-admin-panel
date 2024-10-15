from django.test import TestCase

from movies.models import Person


class PersonModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        # и сохраняем созданную запись в качестве переменной класса
        cls.person = Person.objects.create(
            full_name='Леонардо Вильгельм Ди Каприо'
        )

    def test_types_name(self):
        """Проверка: типы полей совпадает с ожидаемым."""
        person = PersonModelTest.person
        self.assertEqual(person._meta.get_field(
            'full_name').get_internal_type(), 'CharField')

    def test_object_name_is_full_name_fild(self):
        """Проверка: str - это строчка с содержимым person.full_name."""
        person = PersonModelTest.person
        expected_object_name = person.full_name
        self.assertEqual(expected_object_name, str(person))

    def test_db_table(self):
        """Проверка: название таблицы БД совпадает с ожидаемым."""
        person = PersonModelTest.person
        expected_db_table = 'content"."person'
        self.assertEqual(expected_db_table, person._meta.db_table)

    def test_verbose_name_table(self):
        """Проверка: verbose_name совпадает с ожидаемым."""
        person = PersonModelTest.person
        self.assertRegex(str(person._meta.verbose_name), r'[а-яА-Я]+',
                         msg="Имя таблицы должно быть на русском языке.")
        self.assertRegex(str(person._meta.verbose_name_plural), r'[а-яА-Я]+',
                         msg="Имя таблицы должно быть на русском языке.")
