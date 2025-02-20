from django.core.management.base import BaseCommand
from faker import Faker
from events.models import Event, EventParticipants
import random
from datetime import datetime, timedelta
from django.utils.text import slugify

from users.models import User

fake = Faker()


def random_dates_within_month(year, month):
    end_date = datetime(year + 1, 1, 1) - timedelta(days=1) if month == 12 else datetime(year, month + 1,
                                                                                         1) - timedelta(days=1)
    start = fake.date_between_dates(datetime(year, month, 1), end_date.date())
    end = start + timedelta(days=random.choice([3, 4, 5, 7]))
    return start, end


class Command(BaseCommand):
    help = 'Generate fake data for Event Model'

    def add_arguments(self, parser):
        parser.add_argument('num_entries', type=int, help='Number of fake entries to generate')

    def handle(self, *args, **kwargs):
        num_entries = kwargs['num_entries']

        for _ in range(num_entries):
            dates = random_dates_within_month(2025, 2)
            is_online = random.choice([True, False])
            location = None if is_online else fake.address()
            title = fake.paragraph(1)
            organizer = random.choice(User.objects.all())

            event = Event.objects.create(
                title=title,
                slug=slugify(title),
                description=fake.paragraph(random.randint(4, 15)),
                date_start=dates[0],
                date_end=dates[1],
                is_online=is_online,
                location=location,
                status=random.choice([status[0] for status in Event.Status.choices]),
                type=random.choice([event_type[0] for event_type in Event.Type.choices]),
                organizer=organizer
            )

            EventParticipants.objects.create(
                event=event,
                user=organizer
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {num_entries} fake data entries'))
