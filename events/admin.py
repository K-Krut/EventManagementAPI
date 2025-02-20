from tkinter import EventType

from django.contrib import admin

from events.models import Event, EventParticipants


# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'slug', 'description', 'date_start', 'date_end', 'is_online',
        'location', 'status', 'type', 'organizer'
    ]
    list_filter = ['status', 'type', 'is_online', 'date_start', 'date_end']
    search_fields = ['title', 'description']
    ordering = ['status', 'date_start', 'type']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(EventParticipants)
class EventParticipantsAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'registered_at']
    list_filter = ['event', 'user']
    search_fields = ['event__title', 'user__email']
    ordering = ['event']
    show_facets = admin.ShowFacets.ALWAYS
