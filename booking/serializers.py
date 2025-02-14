from rest_framework import serializers
from core.serializers import BaseToRepresentation
from booking.models import BookDoctor


class BookSerializer(BaseToRepresentation, serializers.ModelSerializer):

    class Meta:
        model = BookDoctor
        exclude = ['is_deleted', 'doctor']


class BookDoctoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookDoctor
        fields = ['doctor']


class CloseBookingSerializer(serializers.ModelSerializer):
    booking_id = serializers.UUIDField(source='id')

    class Meta:
        model = BookDoctor
        fields = ['booking_id']
