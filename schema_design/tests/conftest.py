import psycopg
import pytest
import os

DSL = {
    'dbname': os.getenv('POSTGRES_DB', 'movies_database'),
    'user': os.getenv('POSTGRES_USER', 'app'),
    'password': os.getenv('POSTGRES_PASSWORD', '123qwe'),
    'host': os.getenv('SQL_HOST', 'localhost'),
    'port': os.getenv('SQL_PORT', '5432'),
}


@pytest.fixture(scope='session')
def check_file_exists():
    file_path = './movies_database.ddl'
    if not os.path.isfile(file_path):
        pytest.fail(f"Файл с именем '{file_path}' не существует.")
    return file_path


@pytest.fixture(scope='session', autouse=True)
def setup_database(check_file_exists):
    conn = psycopg.connect(
        dbname=DSL['dbname'],
        user=DSL['user'],
        password=DSL['password'],
        host=DSL['host'],
        port=DSL['port'],
    )
    cursor = conn.cursor()

    # Чтение DDL из файла
    with open(check_file_exists, 'r') as ddl_file:
        ddl_commands = ddl_file.read()
    # TODO: think about dropping
    cursor.execute('DROP SCHEMA IF EXISTS content CASCADE;')
    # Выполнение DDL команд
    cursor.execute(ddl_commands)
    conn.commit()
    # Возврат курсора для использования в тестах, если это необходимо
    yield cursor
    # Закрытие соединения после всех тестов
    conn.close()
