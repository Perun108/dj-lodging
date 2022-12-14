"""Module for all serializers related to the lodgings APIs."""

from rest_framework import serializers

from djlodging.api.users.serializers import LodgingUserOutputSerializer


class CountryCreateInputSerializer(serializers.Serializer):
    """Serializer to add a new country."""

    name = serializers.CharField()


class CountryOutputSerializer(serializers.Serializer):
    """Serializer to display a country's details."""

    id = serializers.UUIDField()
    name = serializers.CharField()


class CountryPaginatedOutputSerializer(serializers.Serializer):
    """Serializer to display a paginated list of countries."""

    count = serializers.IntegerField()
    results = CountryOutputSerializer(many=True)


class CountryUpdateInputSerializer(serializers.Serializer):
    """Serializer to accept input to update a country's details."""

    name = serializers.CharField()


class CityCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    region = serializers.CharField(required=False)


class CityUpdateInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    region = serializers.CharField(required=False)


class CityOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    country = CountryOutputSerializer()
    name = serializers.CharField()
    region = serializers.CharField(required=False)


class CityListPaginatedOutputSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = CityOutputSerializer(many=True)


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


class LodgingUpdateInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    kind = serializers.CharField(required=False)
    street = serializers.CharField(required=False)
    house_number = serializers.CharField(required=False)
    zip_code = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    district = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=7, decimal_places=2, min_value=0, required=False)


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
    created = serializers.DateTimeField()


class LodgingOutputSerializer(LodgingCreateOutputSerializer):
    average_rating = serializers.FloatField(required=False)


class LodgingShortOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    kind = serializers.CharField()
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


class LodgingListOutputSerializer(LodgingOutputSerializer):
    available = serializers.BooleanField(required=False)


class LodgingListPaginatedOutputSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = LodgingListOutputSerializer(many=True)


class ReviewCreateInputSerializer(serializers.Serializer):
    lodging_id = serializers.UUIDField()
    reference_code = serializers.CharField()
    text = serializers.CharField()
    score = serializers.IntegerField()


class UserReviewOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    first_name = serializers.CharField()
    nationality = serializers.CharField()


class ReviewOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user = UserReviewOutputSerializer()
    text = serializers.CharField()
    score = serializers.IntegerField()
    created = serializers.DateTimeField()


class ReviewPaginatedListOutputSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = ReviewOutputSerializer(many=True)


class ReviewUpdateInputSerializer(serializers.Serializer):
    text = serializers.CharField()
    score = serializers.IntegerField()


class MyReviewOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    lodging = LodgingShortOutputSerializer()
    text = serializers.CharField()
    score = serializers.IntegerField()
    created = serializers.DateTimeField()


class MyReviewsPaginatedListOutputSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = MyReviewOutputSerializer(many=True)
