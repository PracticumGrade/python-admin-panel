import re

import pytest


def test_uuid_ossp_extension_exists_in_content(setup_database):
    """Проверяет, что расширение uuid-ossp НЕ подключено к схеме content."""

    schema = 'content'
    cursor = setup_database
    cursor.execute(
        "SELECT extname FROM pg_extension WHERE extname = 'uuid-ossp' AND extnamespace = (SELECT oid FROM pg_namespace WHERE nspname = %s)",
        (schema,)
    )
    extensions = cursor.fetchall()
    assert extensions != [('uuid-ossp',)], (
        f'Проверьте, что расширение uuid-ossp НЕ используется в схеме {schema}. Подробнее см. https://postgrespro.ru/docs/postgresql/16/uuid-ossp'
    )

def test_uuid_ossp_extension_exists_in_public(setup_database):
    """Проверяет, что расширение uuid-ossp НЕ подключено к схеме default."""

    schema = 'public'
    cursor = setup_database
    cursor.execute(
        "SELECT extname FROM pg_extension WHERE extname = 'uuid-ossp' AND extnamespace = (SELECT oid FROM pg_namespace WHERE nspname = %s)",
        (schema,)
    )
    extensions = cursor.fetchall()
    assert extensions != [('uuid-ossp',)], (
        f'Проверьте, что расширение uuid-ossp НЕ используется в схеме {schema}. Подробнее см. https://postgrespro.ru/docs/postgresql/16/uuid-ossp'
    )


def test_schema_exists(setup_database):
    """Проверяет, что схема существует."""

    schema = 'content'
    cursor = setup_database
    cursor.execute(
        "SELECT nspname FROM pg_namespace WHERE nspname NOT IN ("
        "'information_schema', 'pg_catalog', 'pg_toast');"
    )
    schemas = cursor.fetchall()
    assert (schema,) in schemas, (
        f'Проверьте, что cхема {schema} существует'
    )


@pytest.mark.parametrize(
    'table_name',
    ('person', 'person_film_work', 'film_work', 'genre', 'genre_film_work')

)
def test_tables_exist(setup_database, table_name):
    """Проверяет, что таблицы в схеме существуют."""

    cursor = setup_database
    cursor.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema='content' AND table_type='BASE TABLE';"
    )
    tables = cursor.fetchall()

    # Здесь необходимо проверить, что ваши таблицы созданы
    table_names = [table[0] for table in tables]
    assert table_name in table_names, (
        f'Проверьте, что таблица {table_name} существует'
    )


@pytest.mark.parametrize(
    'table_name, expected_answers',
    [
        (
                'film_work',
                [['id']]
        ),
        (
                'person',
                [['id']]
        ),
        (
                'person_film_work',
                [['id'], ['film_work_id', 'person_id', 'role']],
        ),
        (
                'genre',
                [['id']],
        ),
        (
                'genre_film_work',
                [['id'], ['film_work_id', 'genre_id']],
        ),
    ]
)
def test_unique_indexes_exist(setup_database, table_name, expected_answers):
    """Проверяет, что уникальные индексы в таблицах существуют."""

    query = f"""
        SELECT indexname, indexdef
        FROM pg_indexes
        WHERE schemaname = 'content' AND tablename = '{table_name}';
    """
    cursor = setup_database
    cursor.execute(query)
    indexes = cursor.fetchall()

    index_defs = [index[1] for index in indexes]

    for expected_fields in expected_answers:
        # Сортировка полей в индексе и ожидаемых полей для сравнения
        expected_fields.sort()

        # Поиск индекса с соответствующими полями и свойством UNIQUE
        found_index = False
        for idx_def in index_defs:
            if "CREATE UNIQUE INDEX" in idx_def:  # Проверка наличия UNIQUE
                columns_match = re.search(
                    r"USING btree \(([A-Za-z0-9_, ]*)\)", idx_def
                )
                if columns_match:
                    columns = columns_match.group(1).split(',')
                    columns = [column.strip() for column in columns]
                    columns.sort()
                    if columns == expected_fields:
                        found_index = True
                        break

        assert found_index, f"В таблице {table_name} должен быть уникальный индекс с полями {expected_fields}"


@pytest.mark.parametrize(
    'table_name, expected_foreign_keys',
    [
        (
                'person_film_work',
                [
                    {'column_name': 'person_id',
                     'foreign_table_name': 'person',
                     'foreign_column_name': 'id'},
                    {'column_name': 'film_work_id',
                     'foreign_table_name': 'film_work',
                     'foreign_column_name': 'id'},
                ]
        ),
        (
                'genre_film_work',
                [
                    {'column_name': 'genre_id', 'foreign_table_name': 'genre',
                     'foreign_column_name': 'id'},
                    {'column_name': 'film_work_id',
                     'foreign_table_name': 'film_work',
                     'foreign_column_name': 'id'},
                ]
        ),
    ]
)
def test_foreign_keys(setup_database, table_name, expected_foreign_keys):
    """Проверяет наличие внешних ключей в таблице."""

    query = f"""
         SELECT DISTINCT
             kcu.column_name,
             ccu.table_name AS foreign_table_name,
             ccu.column_name AS foreign_column_name
         FROM
             information_schema.table_constraints AS tc
         JOIN
             information_schema.key_column_usage AS kcu
             ON tc.constraint_name = kcu.constraint_name
         JOIN
             information_schema.constraint_column_usage AS ccu
             ON ccu.constraint_name = tc.constraint_name
         WHERE
             constraint_type = 'FOREIGN KEY' AND
             tc.table_name = '{table_name}' AND
             tc.table_schema = 'content';
     """
    cursor = setup_database
    cursor.execute(query)

    actual_foreign_keys = [dict(
        zip(('column_name', 'foreign_table_name', 'foreign_column_name'), row))
        for row in cursor.fetchall()]

    set1 = set(tuple(sorted(d.items())) for d in actual_foreign_keys)
    set2 = set(tuple(sorted(d.items())) for d in expected_foreign_keys)

    assert set1 == set2, (
        f"В таблице {table_name} должны быть связи: {format_foreign_key_list(
            expected_foreign_keys
        )}"
    )


def format_foreign_key_list(foreign_keys):
    """Форматирует список внешних ключей для удобного отображения об ошибке."""
    formatted_list = []
    for key in foreign_keys:
        formatted_list.append(
            f" {key['column_name']} -> "
            f"{key['foreign_table_name']}({key['foreign_column_name']})"
        )
    return " | ".join(formatted_list)


@pytest.mark.parametrize(
    'table_name, expected_columns',
    [
        (
                'person',
                {
                    'id': 'uuid',
                    'full_name': 'text',
                    'created': (
                            'timestamp without time zone',
                            'timestamp with time zone'),
                    'modified': (
                            'timestamp without time zone',
                            'timestamp with time zone'),
                }
        ),
        (
                'film_work',
                {
                    'id': 'uuid',
                    'title': 'text',
                    'description': 'text',
                    'creation_date': 'date',
                    'rating': 'real',
                    'type': 'text',
                    'created': (
                            'timestamp without time zone',
                            'timestamp with time zone'),
                    'modified': (
                            'timestamp without time zone',
                            'timestamp with time zone'),
                }
        ),
        (
                'genre',
                {
                    'id': 'uuid',
                    'name': 'text',
                    'description': 'text',
                    'created': (
                            'timestamp without time zone',
                            'timestamp with time zone'),
                    'modified': (
                            'timestamp without time zone',
                            'timestamp with time zone'),
                }
        ),
        (
                'person_film_work',
                {
                    'id': 'uuid',
                    'person_id': 'uuid',
                    'film_work_id': 'uuid',
                    'role': 'text',
                    'created': (
                            'timestamp without time zone',
                            'timestamp with time zone'),
                }
        ),
        (
                'genre_film_work',
                {
                    'id': 'uuid',
                    'genre_id': 'uuid',
                    'film_work_id': 'uuid',
                    'created': (
                            'timestamp without time zone',
                            'timestamp with time zone'),
                }
        ),
    ]
)
def test_columns_info(setup_database, table_name, expected_columns):
    """В таблице присутствуют ожидаемые столбцы с правильными типами данных."""

    query = f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'content' AND table_name = '{table_name}';
    """
    cursor = setup_database
    cursor.execute(query)

    actual_columns_dict = {row[0]: row[1] for row in cursor.fetchall()}

    for key in expected_columns:
        if key in ('created', 'modified'):
            assert_timestamp_type(table_name, key, actual_columns_dict[key])
        else:
            assert actual_columns_dict[key] == expected_columns[key], (
                f"В таблице {table_name}, колонка '{key}' должна быть {expected_columns[key]}, сейчас она {actual_columns_dict[key]}"
            )


def assert_timestamp_type(table_name, key, actual_type):
    assert actual_type in (
        'timestamp without time zone', 'timestamp with time zone'), (
        f"В таблице {table_name}, колонка  '{key}' должна быть TIMESTAMP WITHOUT TIME ZONE или TIMESTAMPTZ, сейчас она {actual_type}"
    )
