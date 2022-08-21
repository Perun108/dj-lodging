from rest_framework import serializers


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


class LodgingCreateOutputSerializer(serializers.Serializer):
    pass
