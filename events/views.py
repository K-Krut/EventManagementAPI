from django.shortcuts import render
from rest_framework import generics


class EventListView(generics.ListCreateAPIView):
    def get_queryset(self):
        pass


class EventMyListView(generics.ListCreateAPIView):
    def get_queryset(self):
        pass


class EventDetailView(generics.ListCreateAPIView):
    def get_queryset(self):
        pass


class EventParticipantsView(generics.ListCreateAPIView):
    def get_queryset(self):
        pass