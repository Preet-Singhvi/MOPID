from rest_framework import serializers
from .models import Event, Reservation
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class EventSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    slots_available = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id','creator','title','description','start_time','end_time','capacity','seats_reserved','slots_available')
        read_only_fields = ('seats_reserved','creator')

    def get_slots_available(self, obj):
        return obj.slots_available()

class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title','description','start_time','end_time','capacity')

class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ('id','user','event','created_at')
