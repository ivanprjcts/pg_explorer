from django.core.management.base import BaseCommand

from pg_explorer.models import PgClass


class Command(BaseCommand):
    help = "Test"

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Your name')

    def handle(self, *args, **options):
        name = options['name']
        pg_class = PgClass.objects.get(name=name)
        self.stdout.write(f'{pg_class.name}, pages={pg_class.pages}, tuples={pg_class.tuples}')
