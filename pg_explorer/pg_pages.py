"""
https://www.postgresql.org/docs/current/storage-page-layout.html
"""

import struct
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PageHeader:
    """
    Contains general information about the page, including free space pointers.
    """
    lsn: int                     # Log Sequence Number (8 bytes)
    checksum: int                # Page checksum (2 bytes)
    flags: int                   # Flags (2 bytes)
    lower: int                   # Offset to start of free space (2 bytes)
    upper: int                   # Offset to end of free space (2 bytes)
    special: int                 # Offset to special space (indexes) (2 bytes)
    page_size_version: int       # page size (2 bytes)
    prune_xid: int               # Oldest unpruned XMAX on page, or zero if none (4 bytes)

    @property
    def lsn_low(self) -> int:
        return self.lsn & 0xFFFFFFFF

    @property
    def lsn_high(self) -> int:
        return self.lsn >> 32

    @property
    def page_size(self) -> int:
        return (self.page_size_version >> 8) * 256

    @property
    def version(self) -> int:
        return self.page_size_version & 0xFF

    @classmethod
    def from_bytes(cls, raw: bytes) -> "PageHeader":
        unpacked = struct.unpack('<QHHHHHHI', raw)
        return PageHeader(*unpacked)


@dataclass
class ItemId:
    """
    Identifier pointing to the actual item.
    """
    offset: int
    length: int
    flags: int

    @classmethod
    def from_bytes(cls, raw: bytes) -> "ItemId":
        (offset_flags_bits, item_length) = struct.unpack('<HH', raw)
        item_offset = offset_flags_bits & 0x1FFF  # lower 13 bits
        item_flags = (offset_flags_bits >> 13) & 0x07  # next 3 bits
        return ItemId(offset=item_offset, length=item_length, flags=item_flags)


@dataclass
class TupleHeader:
    """
    Fixed-size header (occupying 23 bytes on most machines).
    """
    xmin: int           # insert XID stamp (4 bytes)
    xmax: int           # delete XID stamp (4 bytes)
    xcid_or_xvac: int   # space for xcid or xvac (4 bytes)
                        # xcid - Insert and/or delete CID stamp
                        # xvac - XID for VACUUM operation moving a row version
    ctid_block: int     # block of the current TID of this or newer row version (4 bytes)
    ctid_offset: int    # offset of the current TID of this or newer row version (2 bytes)
    infomask2: int      # number of attributes, plus various flag bits (2 bytes)
    infomask: int       # various flag bits (2 bytes)
    hoff: int           # offset to user data (1 byte)

    @classmethod
    def from_bytes(cls, raw: bytes) -> "TupleHeader":
        fields = struct.unpack("<IIIIHHHB", raw)
        return TupleHeader(*fields)


@dataclass
class HeapTuple:
    """
    Item space.
    """
    header: TupleHeader
    data: bytes


@dataclass
class HeapPage:
    """
    Represents the storage layout of a postgres page.
    """
    header: PageHeader
    item_identifiers: List[ItemId]
    items: List[HeapTuple]
    special_area: Optional[bytes] = None  # ordinary tables do not use a special section at all

    PAGE_HEADER_SIZE = 24
    ITEM_ID_SIZE = 4
    HEAP_TUPLE_HEADER_SIZE = 23

    @classmethod
    def from_bytes(cls, raw: bytes) -> "HeapPage":
        # page header
        page_header = PageHeader.from_bytes(raw[:cls.PAGE_HEADER_SIZE])

        # item identifiers
        item_identifiers = []
        items_count = (page_header.lower - cls.PAGE_HEADER_SIZE) // cls.ITEM_ID_SIZE
        for i in range(items_count):
            offset = cls.PAGE_HEADER_SIZE + i * cls.ITEM_ID_SIZE
            item_identifiers.append(
                ItemId.from_bytes(raw[offset:offset + cls.ITEM_ID_SIZE])
            )

        # items
        items = []
        for item_identifier in item_identifiers:
            tuple_header = TupleHeader.from_bytes(
                raw[item_identifier.offset:item_identifier.offset + cls.HEAP_TUPLE_HEADER_SIZE]
            )
            data_start = item_identifier.offset + tuple_header.hoff
            data_end = item_identifier.offset + item_identifier.length
            data = raw[data_start:data_end]

            items.append(
                HeapTuple(header=tuple_header, data=data)
            )

        return HeapPage(header=page_header, item_identifiers=item_identifiers, items=items)
