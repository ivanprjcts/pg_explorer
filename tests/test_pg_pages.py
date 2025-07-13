from pg_explorer.pg_pages import HeapPage


def test_heap_page_from_bytes(page0_bytes):
    page = HeapPage.from_bytes(page0_bytes)

    assert page.header.lower == 28
    assert page.header.upper == 8144
    assert page.header.page_size == 8192
    assert len(page.items) == 1
