from django.core.management.base import BaseCommand

from pg_explorer import pg_utils
from pg_explorer.models import PgClass
from pg_explorer.pg_pages import HeapPage


class Command(BaseCommand):
    help = "Explore Postgres raw data."

    def add_arguments(self, parser):
        parser.add_argument('table_name', type=str, help='Table name')
        parser.add_argument('--page-number', type=int, default=0, help='Page number')

    def summary(self, table_name: str):
        pg_utils.analyze_table(table_name=table_name)  # refresh stats
        pg_class = PgClass.objects.get(name=table_name)
        self.stdout.write(
            f'{pg_class.name}, pages={pg_class.pages}, all_visible={pg_class.rel_all_visible}, '
            f'tuples={pg_class.tuples}'
        )

    def inspect(self, table_name: str, page_number: int):
        raw_page = pg_utils.get_raw_page(table_name=table_name, block_number=page_number)
        page = HeapPage.from_bytes(raw_page)
        header = page.header
        self.stdout.write(
            f'lsn={header.lsn_low:X}/{header.lsn_high:X}, checksum={header.checksum}, flags={header.flags}, '
            f'lower={header.lower}, upper={header.upper}, special={header.special}, page_size={header.page_size}, '
            f'version={header.version}, prune_xid={header.prune_xid}'
        )
        for line in page.item_identifiers:
            self.stdout.write(
                f'offset={line.offset}, length={line.length}, flags={line.flags}'
            )
        for pg_tuple in page.items:
            self.stdout.write(
                f'xmin={pg_tuple.header.xmin}, xmax={pg_tuple.header.xmax}, '
                f'xcid_or_xvac={pg_tuple.header.xcid_or_xvac}, ctid=({pg_tuple.header.ctid_block}, '
                f'{pg_tuple.header.ctid_offset}), infomask2={pg_tuple.header.infomask2}, '
                f'infomask={pg_tuple.header.infomask}, hoff={pg_tuple.header.hoff}, '
                f'data={pg_tuple.data}'
            )

    def handle(self, *args, **options):
        table_name = options['table_name']
        page_number = options['page_number']
        self.summary(table_name)
        self.inspect(table_name, page_number)
