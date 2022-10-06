from rest_framework import serializers

from djlodging.api.users.serializers import LodgingUserOutputSerializer
from djlodging.domain.lodgings.models.lodging import Lodging


class CountryCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField()


class CountryCreateOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()


class CityCreateInputSerializer(serializers.Serializer):
    country_id = serializers.UUIDField()
    name = serializers.CharField()
    region = serializers.CharField(required=False)


class CityOutputSerializer(serializers.Serializer):
    country_id = serializers.UUIDField()
    name = serializers.CharField()
    region = serializers.CharField(required=False)


class LodgingCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    kind = serializers.CharField()
    city_id = serializers.UUIDField()
    street = serializers.CharField()
    house_number = serializers.CharField()
    zip_code = serializers.CharField()
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    district = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=7, decimal_places=2, min_value=0)


class LodgingCountryOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()


class LodgingCityOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    country = LodgingCountryOutputSerializer()
    region = serializers.CharField()


class LodgingOwnerOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()


class LodgingCreateOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    kind = serializers.CharField()
    owner = LodgingUserOutputSerializer()
    city = CityOutputSerializer()
    district = serializers.CharField()
    street = serializers.CharField()
    house_number = serializers.CharField()
    zip_code = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.EmailField()
    number_of_people = serializers.IntegerField()
    number_of_rooms = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)


class LodgingOutputSerializer(LodgingCreateOutputSerializer):
    average_rating = serializers.FloatField(required=False)


class LodgingListOutputSerializer(LodgingOutputSerializer):
    available = serializers.BooleanField(required=False)


class LodgingListInputSerializer(serializers.ModelSerializer):
    """Serializer for query params in the GET request to list all lodgings"""

    city = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    available_only = serializers.BooleanField(default=False)

    class Meta:
        model = Lodging
        fields = [
            "city",
            "country",
            "number_of_people",
            "number_of_rooms",
            "date_from",
            "date_to",
            "available_only",
        ]


class ReviewCreateInputSerializer(serializers.Serializer):
    text = serializers.CharField()
    score = serializers.IntegerField()


class ReviewOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    lodging = LodgingOutputSerializer()
    score = serializers.IntegerField()
