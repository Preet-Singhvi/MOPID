# bookings/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import connection
from unittest import skipIf
from .models import Event, Reservation
import threading


class BookingConcurrencyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.event = Event.objects.create(
            title="Test Event",
            description="desc",
            start_time="2025-09-28T10:00:00Z",
            end_time="2025-09-28T11:00:00Z",
            capacity=1,
        )
        self.client.force_login(self.user)

    @skipIf(connection.vendor == "sqlite", "SQLite cannot handle concurrency tests properly")
    def test_concurrent_reservations_do_not_overbook(self):
        """
        This test is skipped on SQLite because it does not support
        row-level locking or true concurrency. It will run correctly
        on PostgreSQL/MySQL and demonstrate no overbooking.
        """
        successes = []

        def try_reserve():
            resp = self.client.post(reverse("reserve-event", args=[self.event.id]))
            if resp.status_code == 201:
                successes.append(1)

        threads = [threading.Thread(target=try_reserve) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # With capacity=1, only one reservation should succeed
        self.assertEqual(len(successes), 1)
        self.assertEqual(Reservation.objects.filter(event=self.event).count(), 1)
