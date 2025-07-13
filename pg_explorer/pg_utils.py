from django.db import connection


def analyze_table(table_name: str):
    with connection.cursor() as cursor:
        cursor.execute(f"ANALYZE {table_name};")


def get_raw_page(table_name: str, block_number: int) -> bytes:
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT get_raw_page(%s, %s)", [table_name, block_number])
        return cursor.fetchone()[0]  # raw bytea (binary) data
