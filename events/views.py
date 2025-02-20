from rest_framework import generics
from rest_framework import filters, exceptions
from rest_framework.pagination import PageNumberPagination

from events.models import Event
from events.serializers import EventSerializer


class EventPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class EventListView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    pagination_class = EventPagination
    ordering_fields = ['title', 'date_start', 'date_end', 'status', 'type']
    ordering = ['-date_start', 'status', 'type']

    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        queryset = Event.objects.filter(status__in=[Event.Status.ACTIVE, Event.Status.DONE]).order_by(*self.ordering)
        return queryset


class EventMyListView(generics.ListCreateAPIView):
    def get_queryset(self):
        pass


class EventDetailView(generics.ListCreateAPIView):
    def get_queryset(self):
        pass


class EventParticipantsView(generics.ListCreateAPIView):
    def get_queryset(self):
        pass