from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status, permissions
from rest_framework import filters, exceptions
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from events.models import Event, EventParticipants
from events.serializers import EventSerializer, EventDetailsSerializer, ParticipantSerializer, \
    EventParticipantSerializer


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


class EventDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventDetailsSerializer

    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('id')
        try:
            event = Event.objects.get(id=event_id)
            response = self.serializer_class(event, context={'request': request})
            return Response(response.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'errors': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except TimeoutError:
            return Response({'errors': 'Request timeout'}, status=503)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventParticipantsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventParticipantSerializer

    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('id')

        try:
            try:
                event = Event.objects.get(id=event_id)
            except ObjectDoesNotExist:
                return Response({'errors': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

            if not event.organizer == request.user:
                return Response({'errors': 'Access forbidden'}, status=status.HTTP_403_FORBIDDEN)

            participants = EventParticipants.objects.filter(event=event).exclude(user=event.organizer)
            response = self.serializer_class(participants, many=True)

            return Response({
                'participants_number': participants.count(),
                'organizer': ParticipantSerializer(event.organizer).data,
                'participants': response.data,

            }, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'errors': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except TimeoutError:
            return Response({'errors': 'Request timeout'}, status=503)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
