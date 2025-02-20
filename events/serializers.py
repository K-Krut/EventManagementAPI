from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from events.models import Event, EventParticipants
from users.models import User


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class EventParticipantSerializer(serializers.ModelSerializer):
    user = ParticipantSerializer(read_only=True)

    class Meta:
        model = EventParticipants
        fields = ['user', 'registered_at']


class EventSerializer(serializers.ModelSerializer):
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'slug', 'date_start', 'date_end', 'status', 'type', 'is_registered']

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


class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            'title', 'slug', 'date_start', 'date_end', 'description', 'is_online', 'location', 'status', 'type',
            'organizer'
        ]
        read_only_fields = ['organizer', 'slug']

    def validate(self, data):
        if data.get('status') not in Event.Status.values:
            raise ValidationError('Invalid status')

        if data.get('type') not in Event.Type.values:
            raise ValidationError('Invalid type')

        if not data.get('is_online') and not data.get('location'):
            raise ValidationError('Enter location for offline events or mark event as online')

        if not data['date_start'] < data['date_end']:
            raise ValidationError('Event\'s Date Start must be before Date End')

        return data


class EventUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            'title', 'slug', 'date_start', 'date_end', 'description', 'is_online', 'location', 'status', 'type',
            'organizer'
        ]
        read_only_fields = ['organizer', 'slug']

    def validate(self, data):
        if data.get('status'):
            if data.get('status') not in Event.Status.values:
                raise ValidationError('Invalid status')

        if data.get('type'):
            if data.get('type') not in Event.Type.values:
                raise ValidationError('Invalid type')

        if data.get('is_online') or data.get('location'):
            if not data.get('is_online') and not data.get('location'):
                raise ValidationError('Enter location for offline events or mark event as online')

        instance = self.instance
        date_start = data.get('date_start', instance.date_start)
        date_end = data.get('date_end', instance.date_end)

        if not date_start < date_end:
            raise ValidationError('Event\'s Date Start must be before Date End')

        return data
