from django.test import TestCase


class MixinTest(TestCase):
    def test_mixins_file_exists(self):
        """Проверка: файл mixins.py существует."""

        try:
            from movies.mixins import TimeStampedMixin, UUIDMixin
        except ImportError:
            self.fail(
                "Поместите UUIDMixin и TimeStampedMixin в файл с именем "
                "mixins.py рядом с models.py "
            )
