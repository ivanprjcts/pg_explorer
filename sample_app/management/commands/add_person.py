import random

from django.core.management.base import BaseCommand

from sample_app.models import Person


class Command(BaseCommand):
    help = "Add new people to DB"

    def handle(self, *args, **options):
        name_choices = ['Ivan', 'Alfonso', 'Marcos', 'Rosa', 'Jose']
        name = random.choice(name_choices)
        age = random.randint(1, 100)

        # add new object
        Person.objects.create(name=name, age=age)
        self.stdout.write(self.style.SUCCESS(f'Person ({name=}, {age=}) successfully added'))
