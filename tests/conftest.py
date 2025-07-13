import binascii
import pathlib

import pytest


@pytest.fixture
def page0_bytes():
    hex_data = pathlib.Path("tests/fixtures/page0.hex").read_text().strip()
    return binascii.unhexlify(hex_data)
