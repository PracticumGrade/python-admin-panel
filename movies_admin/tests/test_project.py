import os
import unittest

from django.conf import settings
from django.utils.version import get_version


class ProjectStructureTest(unittest.TestCase):

    def test_project_directory_exists(self):
        """Проверка: наличие требуемой папки."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        expected_dirs = ('movies', 'config')
        for one_expected_dir in expected_dirs:
            with self.subTest(field=one_expected_dir):
                self.assertTrue(
                    os.path.isdir(one_expected_dir),
                    f'В директории {base_dir} не найдена папка с '
                    f'проектом {one_expected_dir}. Убедитесь, что у вас '
                    'верная структура проекта.'
                )

    def test_migrations_exists(self):
        """Проверка: наличие папки с миграциями."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        migrations_dir = os.path.join(base_dir, 'movies', 'migrations')
        self.assertTrue(
            os.path.isdir(migrations_dir),
            'В директории movies не найдена папка с '
            'миграциями - migrations. Создайте миграции '
            'командой: '
            'python manage.py makemigrations movies --settings=config.settings'
        )

    def test_locale_exists(self):
        """Проверка: наличие папки с локализацией."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        migrations_dir = os.path.join(base_dir, 'movies', 'locale')
        self.assertTrue(
            os.path.isdir(migrations_dir),
            'В директории movies не найдена папка с локализаций - locale.'
            'Создайте ее, добавьте строку в settings.py: '
            'LOCALE_PATHS = ["movies/locale"]. После этого выполните команду: '
            'python manage.py makemessages -l en -l ru )'
        )

    def test_manage_py_exists(self):
        """Проверка: наличие файла manage.py."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        filename = 'manage.py'
        self.assertTrue(os.path.isfile(os.path.join(base_dir, filename)),
                        f'В директории {base_dir} не найден файл '
                        f'{filename}. Убедитесь, что у вас верная структура '
                        'проекта.'
                        )


class DjangoVersionTest(unittest.TestCase):

    def test_django_version(self):
        """Проверка: версия Django."""
        self.assertGreater(
            get_version(),
            '4.0.0',
            'Пожалуйста, используйте версию Django > 4.0.0')


class AppRegistrationTest(unittest.TestCase):

    def test_app_registration(self):
        """Проверка: регистрация приложения в INSTALLED_APPS."""
        self.assertTrue(
            any(
                app in settings.INSTALLED_APPS for app in [
                    'movies.apps.MoviesConfig',
                    'movies']),
            'Пожалуйста зарегистрируйте приложение в '
            'settings.INSTALLED_APPS')
