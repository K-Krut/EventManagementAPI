from django.core.management.base import BaseCommand
from faker import Faker
from events.models import Event

fake = Faker()


class Command(BaseCommand):
    help = 'Generate fake data for Event Model'

    def add_arguments(self, parser):
        parser.add_argument('num_entries', type=int, help='Number of fake entries to generate')

    def handle(self, *args, **kwargs):
        num_entries = kwargs['num_entries']

        for _ in range(num_entries):
            Event.objects.create(
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {num_entries} fake data entries'))