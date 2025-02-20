from django.core.management.base import BaseCommand
from events.models import Event, EventParticipants
import random
from users.models import User


class Command(BaseCommand):
    help = 'Generate fake data for EventParticipants Model'

    def handle(self, *args, **kwargs):

        events = Event.objects.exclude(status=Event.Status.ACTIVE)

        for event in events:
            organizer_is_participant = EventParticipants.objects.filter(user=event.organizer, event=event)

            if not organizer_is_participant:
                EventParticipants.objects.create(
                    event=event,
                    user=event.organizer
                )
            print('organizer_is_participant: ', organizer_is_participant)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated fake data entries'))
