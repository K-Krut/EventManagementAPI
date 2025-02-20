from django.core.management.base import BaseCommand
from events.models import Event, EventParticipants
import random
from users.models import User


class Command(BaseCommand):
    help = 'Generate fake data for EventParticipants Model'

    def handle(self, *args, **kwargs):

        active_events = Event.objects.filter(status=Event.Status.ACTIVE)
        users = User.objects.filter(is_active=True)
        maximum_possible_participants = len(users) - 1

        for event in active_events:
            possible_participants = list(users.exclude(id=event.organizer.id))
            number_of_participants = random.randint(1, maximum_possible_participants)
            participants = random.sample(possible_participants, number_of_participants)
            for participant in participants:
                EventParticipants.objects.create(
                    event=event,
                    user=participant
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated fake data entries'))
