import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APIClient

from djlodging.domain.lodgings.models import City
from tests.domain.lodgings.factories import CityFactory

fake = Faker()


@pytest.mark.django_db
class TestDeleteCity:
    def test_delete_city_succeeds(self, admin_api_client_factory_boy):
        city = CityFactory()
        country_id = str(city.country.id)
        city_id = str(city.id)

        url = reverse(
            "cities-detail", args=[country_id, city_id]
        )  # FIXME add country_id to all these urls - POST "/api/cities/"
        response = admin_api_client_factory_boy.delete(url)

        assert response.status_code == HTTP_204_NO_CONTENT
        assert response.data is None

        assert City.objects.first() is None

    def test_delete_city_by_regular_user_fails(self, user_api_client_factory_boy):
        city = CityFactory()
        country_id = str(city.country.id)
        city_id = str(city.id)

        url = reverse(
            "cities-detail", args=[country_id, city_id]
        )  # FIXME add country_id to all these urls - POST "/api/cities/"
        response = user_api_client_factory_boy.delete(url)

        assert response.status_code == HTTP_403_FORBIDDEN
        assert str(response.data["detail"]) == "You do not have permission to perform this action."

        assert City.objects.first() == city

    def test_delete_city_by_unauthenticated_admin_fails(self):
        city = CityFactory()
        country_id = str(city.country.id)
        city_id = str(city.id)

        api_client = APIClient()
        url = reverse(
            "cities-detail", args=[country_id, city_id]
        )  # FIXME add country_id to all these urls - POST "/api/cities/"
        response = api_client.delete(url)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == "Authentication credentials were not provided."

        assert City.objects.first() == city
