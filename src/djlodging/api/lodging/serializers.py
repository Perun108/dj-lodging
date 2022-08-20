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
