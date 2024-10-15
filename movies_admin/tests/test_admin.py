from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from movies.admin import (FilmworkAdmin, GenreAdmin, GenreFilmworkInline,
                          PersonAdmin, PersonFilmworkInline)
from movies.models import Filmwork, Genre, Person


class AdminTests(TestCase):
    def test_genre_admin_search_fields(self):
        """Проверка: в админке GenreAdmin доступны поля поиска."""
        admin_site = AdminSite()
        genre_admin = GenreAdmin(Genre, admin_site)
        self.assertEqual(
            genre_admin.search_fields,
            ('name',),
            "Сделайте поиск (search_fields) по полю  name"
        )

    def test_person_admin_search_fields(self):
        """Проверка: В админке PersonAdmin доступны поля поиска."""
        admin_site = AdminSite()
        person_admin = PersonAdmin(Person, admin_site)
        self.assertEqual(
            person_admin.search_fields,
            ('full_name',),
            'Сделайте поиск (search_fields) по полю  full_name'
        )

    def test_filmwork_admin_inlines(self):
        """Проверка: в админке FilmWorkAdmin есть правильные инлайны."""
        admin_site = AdminSite()
        filmwork_admin = FilmworkAdmin(Filmwork, admin_site)
        self.assertIn(
            PersonFilmworkInline,
            filmwork_admin.inlines,
            "В админке FilmWorkAdmin есть инлайн PersonFilmWorkInline"
        )
        self.assertIn(
            GenreFilmworkInline,
            filmwork_admin.inlines,
            "В админке FilmWorkAdmin есть инлайн GenreFilmWorkInline"
        )

    def test_filmwork_admin_list_display(self):
        """Проверка: в админке FilmWorkAdmin отображаются правильные поля."""
        admin_site = AdminSite()
        filmwork_admin = FilmworkAdmin(Filmwork, admin_site)
        # Проверка наличия обязательных полей
        self.assertIn('title', filmwork_admin.list_display)
        self.assertIn('creation_date', filmwork_admin.list_display)
        self.assertIn('rating', filmwork_admin.list_display)
        self.assertIn('type', filmwork_admin.list_display)

    def test_filmwork_admin_list_filter(self):
        """Проверка: в админке FilmWorkAdmin доступны правильные фильтры."""
        admin_site = AdminSite()
        filmwork_admin = FilmworkAdmin(Filmwork, admin_site)
        self.assertEqual(filmwork_admin.list_filter, ('type', 'genres'))

    def test_filmwork_admin_search_fields(self):
        """Проверка: в админке FilmWorkAdmin доступны поля поиска,
        включая 'title', 'description', 'id', и потенциально другие поля.
        """
        admin_site = AdminSite()
        filmwork_admin = FilmworkAdmin(Filmwork, admin_site)
        # Проверка наличия обязательных полей
        self.assertIn('title', filmwork_admin.search_fields)
        self.assertIn('description', filmwork_admin.search_fields)
        self.assertIn('id', filmwork_admin.search_fields)
