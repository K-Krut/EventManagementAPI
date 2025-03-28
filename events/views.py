from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from rest_framework import generics, status
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from events.models import Event, EventParticipants
from events.serializers import EventSerializer, EventDetailsSerializer, ParticipantSerializer, \
    EventParticipantSerializer, EventCreateSerializer, EventUpdateSerializer


class EventPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class EventListView(generics.ListCreateAPIView):
    pagination_class = EventPagination
    ordering_fields = ['title', 'date_start', 'date_end', 'status', 'type']
    ordering = ['-date_start', 'status', 'type']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventCreateSerializer
        return EventSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        try:
            return Event.objects.filter(status__in=[Event.Status.ACTIVE, Event.Status.DONE]).order_by(*self.ordering)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        try:
            event = serializer.save(organizer=self.request.user)
            response = EventSerializer(event, context={'request': self.request})
            return Response(response.data, status=status.HTTP_201_CREATED)
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
            queryset = Event.objects.filter(organizer=user) | Event.objects.filter(event__user=user, event__status__in=[Event.Status.ACTIVE, Event.Status.DONE])
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

    def delete(self, request, *args, **kwargs):
        event_id = kwargs.get('id')

        try:
            event = Event.objects.get(id=event_id)

            if not request.user == event.organizer:
                return Response({'errors': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

            if event.status is Event.Status.DONE:
                return Response({'errors': 'Finished Events can\'t be deleted'}, status=status.HTTP_400_BAD_REQUEST)

            participants = EventParticipants.objects.filter(event=event).exclude(user=event.organizer).exists()
            if event.status is Event.Status.ACTIVE and participants:
                return Response(
                    {'errors': 'Active event with registered users can\'t be deleted'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            return Response({'errors': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except TimeoutError:
            return Response({'errors': 'Request timeout'}, status=503)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        event_id = kwargs.get('id')

        try:
            event = Event.objects.get(id=event_id)

            if not request.user == event.organizer:
                return Response({'errors': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

            if event.status is Event.Status.DONE:
                return Response({'errors': 'Finished Events can\'t be updated'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = EventCreateSerializer(event, data=request.data)

            if serializer.is_valid():
                event = serializer.save()
                response = self.serializer_class(event, context={'request': request})
                return Response(response.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'errors': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch(self, request, *args, **kwargs):
        event_id = kwargs.get('id')

        try:
            event = Event.objects.get(id=event_id)

            if not request.user == event.organizer:
                return Response({'errors': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

            if event.status is Event.Status.DONE:
                return Response({'errors': 'Finished Events can\'t be updated'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = EventUpdateSerializer(event, data=request.data, partial=True)

            if serializer.is_valid():

                event = serializer.save()

                response = self.serializer_class(event, context={'request': request})
                return Response(response.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'errors': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventParticipantsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventParticipantSerializer
    pagination_class = EventPagination

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
