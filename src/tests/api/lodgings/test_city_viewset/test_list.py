import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from rest_framework.test import APIClient

from tests.domain.lodgings.factories import CityFactory, CountryFactory

fake = Faker()


@pytest.mark.django_db
class TestListCity:
    def test_list_cities_succeeds(self, admin_api_client_factory_boy):
        country = CountryFactory()
        country_id = str(country.id)

        number_of_cities = 3
        CityFactory.create_batch(size=number_of_cities, country=country)

        url = reverse(
            "cities-list", args=[country_id]
        )  # FIXME add country_id to all these urls - POST "/api/cities/"
        response = admin_api_client_factory_boy.get(url)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == number_of_cities

    def test_list_cities_by_regular_user_fails(self, user_api_client_factory_boy):
        country = CountryFactory()
        country_id = str(country.id)

        number_of_cities = 3
        CityFactory.create_batch(size=number_of_cities, country=country)

        url = reverse(
            "cities-list", args=[country_id]
        )  # FIXME add country_id to all these urls - POST "/api/cities/"
        response = user_api_client_factory_boy.get(url)

        assert response.status_code == HTTP_403_FORBIDDEN
        assert str(response.data["detail"]) == "You do not have permission to perform this action."

    def test_list_cities_by_unauthenticated_admin_fails(self):
        country = CountryFactory()
        country_id = str(country.id)

        number_of_cities = 3
        CityFactory.create_batch(size=number_of_cities, country=country)

        api_client = APIClient()
        url = reverse(
            "cities-list", args=[country_id]
        )  # FIXME add country_id to all these urls - POST "/api/cities/"
        response = api_client.get(url)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == "Authentication credentials were not provided."
