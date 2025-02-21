from django.core.management.base import BaseCommand
from faker import Faker

from users.models import User

fake = Faker()



class Command(BaseCommand):
    help = 'Generate fake data for User Model'

    def add_arguments(self, parser):
        parser.add_argument('num_entries', type=int, help='Number of fake entries to generate')

    def handle(self, *args, **kwargs):
        num_entries = kwargs['num_entries']

        for _ in range(num_entries):
            try:
                user = User.objects.create(
                    email=fake.email(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    password=fake.password(),
                )
                print(user)
            except Exception as error:
                print(error)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {num_entries} fake data entries'))
