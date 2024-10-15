import os
import sqlite3
import subprocess

import psycopg
import pytest
from dotenv import load_dotenv

load_dotenv()

DSL = {
    'dbname': os.getenv('POSTGRES_DB', 'movies_database'),
    'user': os.getenv('POSTGRES_USER', 'app'),
    'password': os.getenv('POSTGRES_PASSWORD', '123qwe'),
    'host': os.getenv('SQL_HOST', 'localhost'),
    'port': os.getenv('SQL_PORT', '5432'),
}

TABLES = (
    'film_work',
    'person',
    'genre',
    'person_film_work',
    'genre_film_work',
)


@pytest.fixture
def setup_databases():
    sqlite_conn = sqlite3.connect("db.sqlite")
    pg_conn = psycopg.connect(**DSL)
    yield sqlite_conn, pg_conn
    sqlite_conn.close()
    pg_conn.close()


def load_data_script():
    # Запускаем скрипт load_data.py
    subprocess.run(['python', 'load_data.py'], check=True)


def test_data_count(setup_databases):
    """Проверяет, что кол-во данных одинаково в SQLite и PostgreSQL."""
    sqlite_conn, pg_conn = setup_databases
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()

    # Запускаем загрузку данных первый раз
    load_data_script()

    for table_name in TABLES:
        sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        sqlite_count = sqlite_cursor.fetchone()[0]
        pg_cursor.execute(f"SELECT COUNT(*) FROM content.{table_name};")
        pg_count = pg_cursor.fetchone()[0]
        assert sqlite_count == pg_count, (
            f"количество строк в {table_name} "
            f"не одинаковое в SQLite и PostgreSQL."
        )


def test_load_data(setup_databases):
    """Проверяет, что кол-во данных одинаково в SQLite и PostgreSQL после
    повторного запуска."""
    sqlite_conn, pg_conn = setup_databases
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()

    # Запускаем загрузку данных первый раз
    load_data_script()

    # Проверяем количество строк после первого запуска
    sqlite_counts = {}
    pg_counts = {}

    for table_name in TABLES:
        sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        sqlite_counts[table_name] = sqlite_cursor.fetchone()[0]

        pg_cursor.execute(f"SELECT COUNT(*) FROM content.{table_name};")
        pg_counts[table_name] = pg_cursor.fetchone()[0]
    # Сохраняем ожидаемое количество строк
    expected_counts = {
        table: count for table, count in sqlite_counts.items()
    }
    # Запускаем загрузку данных повторно
    load_data_script()
    # Проверяем количество строк после второго запуска
    for table_name in TABLES:
        sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        sqlite_count = sqlite_cursor.fetchone()[0]

        pg_cursor.execute(f"SELECT COUNT(*) FROM content.{table_name};")
        pg_count = pg_cursor.fetchone()[0]

        assert sqlite_count == expected_counts[table_name], (
            f"количество строк в {table_name} "
            f"не одинаковое в SQLite после повторного запуска."
        )
        assert pg_count == expected_counts[table_name], (
            f"количество строк в {table_name} "
            f"не одинаковое в PostgreSQL после повторного запуска."
        )
