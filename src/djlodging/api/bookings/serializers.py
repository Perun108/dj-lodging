"""Serializers for bookings management"""

from rest_framework import serializers

from djlodging.api.lodging.serializers import LodgingOutputSerializer


class BookingCreateInputSerializer(serializers.Serializer):
    """
    Serializer for input parameters to book a lodging.
    """

    lodging_id = serializers.UUIDField()
    date_from = serializers.DateField()
    date_to = serializers.DateField()


class BookingOutputSerializer(serializers.Serializer):
    """
    Serializer to retrieve a booking.
    """

    id = serializers.UUIDField()
    lodging = LodgingOutputSerializer()
    user_id = serializers.UUIDField()
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    status = serializers.CharField()


class BookingListOutputSerializer(serializers.Serializer):
    """
    Serializer to list bookings.
    """

    id = serializers.UUIDField()
    lodging = LodgingOutputSerializer()
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    status = serializers.CharField()
    created = serializers.DateTimeField()


class BookingListPaginatedOutputSerializer(serializers.Serializer):
    """
    Serializer with pagination to list bookings.
    """

    count = serializers.IntegerField()
    results = BookingListOutputSerializer(many=True)


class BookingPayInputSerializer(serializers.Serializer):
    """
    Serializer for input parameters to pay for booking.
    """

    currency = serializers.CharField(required=False)
    capture_method = serializers.CharField(required=False)
