from rest_framework import serializers

from events.models import Event, EventParticipants
from users.models import User


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class EventSerializer(serializers.ModelSerializer):

    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'date_start', 'date_end', 'status', 'type', 'is_registered', ]

    def get_is_registered(self, obj):
        user = self.context['request'].user

        return False if not user.is_authenticated else EventParticipants.objects.filter(user=user, event=obj).exists()


class EventDetailsSerializer(serializers.ModelSerializer):

    organizer = ParticipantSerializer(read_only=True)
    is_registered = serializers.SerializerMethodField()
    participants_number = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'date_start', 'date_end', 'description', 'is_online', 'location', 'status', 'type',
            'is_registered', 'participants_number', 'organizer'
        ]

    def get_is_registered(self, obj):
        user = self.context['request'].user

        return False if not user.is_authenticated else EventParticipants.objects.filter(user=user, event=obj).exists()

    def get_participants_number(self, obj):
        return EventParticipants.objects.filter(event=obj).count()