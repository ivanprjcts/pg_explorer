import random

from django.core.management.base import BaseCommand

from sample_app.models import Person


class Command(BaseCommand):
    help = "List people in DB"

    def handle(self, *args, **options):
        for person in Person.objects.order_by('pk'):
            self.stdout.write(f'{person.pk}, {person.name}, {person.age}')
