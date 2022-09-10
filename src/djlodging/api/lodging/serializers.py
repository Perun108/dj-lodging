from rest_framework import serializers

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


class CityCreateOutputSerializer(serializers.Serializer):
    country_id = serializers.UUIDField()
    name = serializers.CharField()
    region = serializers.CharField(required=False)


class LodgingCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
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


class LodgingOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    type = serializers.CharField()
    owner = LodgingOwnerOutputSerializer()
    city = LodgingCityOutputSerializer()
    district = serializers.CharField()
    street = serializers.CharField()
    house_number = serializers.CharField()
    zip_code = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.EmailField()
    number_of_people = serializers.IntegerField()
    number_of_rooms = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)


class AvailableLodgingListInputSerializer(serializers.ModelSerializer):
    city = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    date_from = serializers.DateField()
    date_to = serializers.DateField()

    class Meta:
        model = Lodging
        fields = ["city", "country", "number_of_people", "number_of_rooms", "date_from", "date_to"]


class AvailableLodgingListOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lodging
        fields = "__all__"
