from rest_framework import serializers

from djlodging.api.lodging.serializers import LodgingOutputSerializer


class BookingCreateInputSerializer(serializers.Serializer):
    lodging_id = serializers.UUIDField()
    date_from = serializers.DateField()
    date_to = serializers.DateField()


class BookingOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    lodging = LodgingOutputSerializer()
    user_id = serializers.UUIDField()
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    status = serializers.CharField()


class BookingListOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    lodging = LodgingOutputSerializer()
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    status = serializers.CharField()
    created = serializers.DateTimeField()


class BookingListPaginatedOutputSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = BookingListOutputSerializer(many=True)


class BookingPayInputSerializer(serializers.Serializer):
    currency = serializers.CharField(required=False)
    capture_method = serializers.CharField(required=False)
