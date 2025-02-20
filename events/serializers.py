from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'date_start', 'date_end', 'description', 'is_online', 'location', 'status', 'type',
            'organizer'
        ]