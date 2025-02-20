from django.urls import path

from events.views import EventListView, EventMyListView, EventDetailView, EventParticipantsView

urlpatterns = [
    path('events/', EventListView.as_view(), name='events_all'),
    path('events/my/', EventMyListView.as_view(), name='events_my'),
    path('events/<int:id>/', EventDetailView.as_view(), name='event-details'),
    path('events/<int:id>/participants/', EventParticipantsView.as_view(), name='event-participants'),
]