from rest_framework import generics, status, permissions
from rest_framework import filters, exceptions
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']

    def get_queryset(self):
        try:
            return Event.objects.filter(status__in=[Event.Status.ACTIVE, Event.Status.DONE]).order_by(*self.ordering)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventMyListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    pagination_class = EventPagination
    ordering_fields = ['title', 'date_start', 'date_end', 'status', 'type']
    ordering = ['-date_start', 'status', 'type']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']

    def get_queryset(self):
        user = self.request.user
        try:
            queryset = Event.objects.filter(organizer=user) | Event.objects.filter(event__user=user)
            return queryset.distinct().order_by(*self.ordering)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventDetailView(generics.ListCreateAPIView):
    def get_queryset(self):
        pass


class EventParticipantsView(generics.ListCreateAPIView):
    def get_queryset(self):
        pass