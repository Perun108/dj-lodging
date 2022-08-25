from rest_framework import serializers

from djlodging.api.lodging.serializers import LodgingOutputSerializer


class BookingCreateInputSerializer(serializers.Serializer):
    lodging_id = serializers.UUIDField()
    date_from = serializers.DateField()
    date_to = serializers.DateField()


class BookingCreateOutputSerializer(serializers.Serializer):
    lodging_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    date_from = serializers.DateField()
    date_to = serializers.DateField()


class BookingListOutputSerializer(serializers.Serializer):
    lodging = LodgingOutputSerializer()
    date_from = serializers.DateField()
    date_to = serializers.DateField()
