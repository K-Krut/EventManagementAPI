from django.db import models

from users.models import User


class Event(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'Draft'
        ACTIVE = 'Active'
        CANCELED = 'Canceled'
        DONE = 'Done'

    class Type(models.TextChoices):
        PUBLIC = 'Public'
        PRIVATE = 'Private'

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    is_online = models.BooleanField(default=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(choices=Status, default=Status.DRAFT, max_length=10)
    type = models.CharField(choices=Type, default=Type.PUBLIC, max_length=10)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_start']
        indexes = [
            models.Index(fields=['-date_start']),
        ]

    def __str__(self):
        return self.title


class EventParticipants(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registered_at']
        unique_together = ('event', 'user')

    def __str__(self):
        return f'{self.event.title} - {self.user.first_name} {self.user.last_name}'

