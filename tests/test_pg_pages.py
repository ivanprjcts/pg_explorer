from pg_explorer.pg_pages import HeapPage


def test_heap_page_from_bytes(page0_bytes):
    page = HeapPage.from_bytes(page0_bytes)

    assert page.header.lower == 28
    assert page.header.upper == 8144
    assert page.header.page_size == 8192
    assert len(page.items) == 1


def test_heap_page_header_fields(page0_bytes):
    page = HeapPage.from_bytes(page0_bytes)
    header = page.header

    assert hasattr(header, "lower")
    assert hasattr(header, "upper")
    assert hasattr(header, "page_size")
    assert isinstance(header.lower, int)
    assert isinstance(header.upper, int)
    assert isinstance(header.page_size, int)

def test_heap_page_items_content(page0_bytes):
    page = HeapPage.from_bytes(page0_bytes)
    assert len(page.items) > 0
    item = page.items[0]
    assert hasattr(item, "offset")
    assert hasattr(item, "length")
    assert item.length > 0