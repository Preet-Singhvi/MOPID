from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Event(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    seats_reserved = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_time']

    def slots_available(self):
        return max(0, self.capacity - self.seats_reserved)

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-created_at']

    def __str__(self):
        return f"Reservation: {self.user} -> {self.event}"
