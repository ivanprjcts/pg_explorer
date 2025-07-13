from django.db import connection


def analyze_table(table_name: str):
    """
    Collects statistics about the contents of the table in the database, and stores the results in
    the pg_statistic system catalog.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"ANALYZE {table_name};")


def get_raw_page(table_name: str, block_number: int) -> bytes:
    """
    Reads the specified block of the named relation and returns a copy as a bytea value.

    It requires 'pageinspect' extension.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT get_raw_page(%s, %s)", [table_name, block_number])
        return cursor.fetchone()[0]
