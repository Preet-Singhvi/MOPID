from django.urls import path
from .views import (
    EventListCreateView,
    EventRetrieveUpdateDestroyView,
    ReserveEventView,
    CancelReservationView,
    MyReservationsView,
    EventReservationsListView,
)

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventRetrieveUpdateDestroyView.as_view(), name='event-detail'),
    path('events/<int:pk>/reservations/', EventReservationsListView.as_view(), name='event-reservations'),
    path('events/<int:pk>/reserve/', ReserveEventView.as_view(), name='event-reserve'),

    path('reservations/', MyReservationsView.as_view(), name='my-reservations'),
    path('reservations/<int:pk>/', CancelReservationView.as_view(), name='cancel-reservation'),
]
