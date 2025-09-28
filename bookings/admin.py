from django.contrib import admin
from .models import Event, Reservation

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','title','creator','start_time','end_time','capacity','seats_reserved')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id','user','event','created_at')
