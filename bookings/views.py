from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction, IntegrityError
from django.db.models import F
from .models import Event, Reservation
from .serializers import EventSerializer, EventCreateUpdateSerializer, ReservationSerializer
from .permissions import IsCreatorOrReadOnly

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().select_related('creator')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventCreateUpdateSerializer
        return EventSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all().select_related('creator')
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT','PATCH']:
            return EventCreateUpdateSerializer
        return EventSerializer

class MyReservationsView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).select_related('event')

class EventReservationsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationSerializer

    def get_queryset(self):
        event_id = self.kwargs['pk']
        return Reservation.objects.filter(event_id=event_id).select_related('user')

class ReserveEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            with transaction.atomic():
                updated = Event.objects.filter(pk=pk, seats_reserved__lt=F('capacity')).update(seats_reserved=F('seats_reserved') + 1)
                if updated == 0:
                    return Response({'detail': 'Event is full.'}, status=status.HTTP_400_BAD_REQUEST)
                reservation = Reservation.objects.create(user=user, event_id=pk)
                serializer = ReservationSerializer(reservation)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'detail': 'You have already reserved this event.'}, status=status.HTTP_400_BAD_REQUEST)

class CancelReservationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        user = request.user
        try:
            with transaction.atomic():
                reservation = Reservation.objects.select_related('event').get(pk=pk, user=user)
                Event.objects.filter(pk=reservation.event_id).update(seats_reserved=F('seats_reserved') - 1)
                reservation.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Reservation.DoesNotExist:
            return Response({'detail': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)
