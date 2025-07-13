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
class LinePointer:
    offset: int
    length: int
    flags: int

    @classmethod
    def from_bytes(cls, raw: bytes) -> "LinePointer":
        (lp_raw,) = struct.unpack('<I', raw)
        lp_offset = lp_raw & 0x1FFF  # lower 13 bits
        lp_flags = (lp_raw >> 13) & 0x07  # next 3 bits
        lp_length = (lp_raw >> 16) & 0xFFFF  # upper 16 bits
        return LinePointer(offset=lp_offset, length=lp_length, flags=lp_flags)


@dataclass
class TupleHeader:
    xmin: int
    xmax: int
    xcid: int
    ctid_block: int
    ctid_offset: int
    infomask2: int
    infomask: int
    hoff: int

    @classmethod
    def from_bytes(cls, raw: bytes) -> "TupleHeader":
        fields = struct.unpack("<IIIIHHHB", raw)
        return TupleHeader(*fields)


@dataclass
class HeapTuple:
    header: TupleHeader
    data: bytes


@dataclass
class HeapPage:
    header: PageHeader
    line_pointers: List[LinePointer]
    tuples: List[HeapTuple]
    special_area: Optional[bytes] = None

    PAGE_HEADER_SIZE = 24
    LINE_POINTER_SIZE = 4
    HEAP_TUPLE_HEADER_SIZE = 23

    @classmethod
    def from_bytes(cls, raw: bytes) -> "HeapPage":
        # page header
        page_header = PageHeader.from_bytes(raw[:cls.PAGE_HEADER_SIZE])

        # line pointers
        line_pointers = []
        num_pointers = (page_header.lower - cls.PAGE_HEADER_SIZE) // cls.LINE_POINTER_SIZE
        for i in range(num_pointers):
            offset = cls.PAGE_HEADER_SIZE + i * cls.LINE_POINTER_SIZE
            line_pointers.append(
                LinePointer.from_bytes(raw[offset:offset + 4])
            )

        # tuples
        tuples = []
        for line_pointer in line_pointers:
            tuple_header = TupleHeader.from_bytes(
                raw[line_pointer.offset:line_pointer.offset + cls.HEAP_TUPLE_HEADER_SIZE]
            )
            data_start = line_pointer.offset + tuple_header.hoff
            data_end = line_pointer.offset + line_pointer.length
            data = raw[data_start:data_end]

            tuples.append(
                HeapTuple(header=tuple_header, data=data)
            )

        return HeapPage(header=page_header, line_pointers=line_pointers, tuples=tuples)
