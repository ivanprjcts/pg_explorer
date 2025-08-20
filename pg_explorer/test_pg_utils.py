import pytest
from unittest import mock
from pg_explorer import pg_utils

@pytest.fixture
def mock_cursor():
    with mock.patch("pg_explorer.pg_utils.connection.cursor") as mock_cursor_ctx:
        yield mock_cursor_ctx

def test_analyze_table_executes_analyze(mock_cursor):
    table_name = "my_table"
    cursor_instance = mock_cursor.return_value.__enter__.return_value
    pg_utils.analyze_table(table_name)
    cursor_instance.execute.assert_called_once_with(f"ANALYZE {table_name};")

def test_get_raw_page_returns_bytes(mock_cursor):
    table_name = "my_table"
    block_number = 5
    expected_bytes = b"pagebytes"
    cursor_instance = mock_cursor.return_value.__enter__.return_value
    cursor_instance.fetchone.return_value = [expected_bytes]
    result = pg_utils.get_raw_page(table_name, block_number)
    cursor_instance.execute.assert_called_once_with(
        "SELECT get_raw_page(%s, %s)", [table_name, block_number]
    )
    assert result == expected_bytes