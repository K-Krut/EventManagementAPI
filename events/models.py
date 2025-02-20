from django.db import models

from users.models import User


# Create your models here.
class Event(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'Draft'
        ACTIVE = 'Active'
        CANCELED = 'Canceled'
        DONE = 'Done'

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    location = models.CharField(max_length=255)
    status = models.CharField(choices=Status, default=Status.DRAFT)
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
