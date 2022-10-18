import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from rest_framework.test import APIClient

from djlodging.domain.lodgings.models import City
from tests.domain.lodgings.factories import CityFactory

fake = Faker()


@pytest.mark.django_db
class TestUpdateCity:
    def test_update_city_succeeds(self, admin_api_client_factory_boy):
        city = CityFactory()
        country_id = str(city.country.id)
        city_id = str(city.id)

        old_name = city.name
        new_name = fake.city()
        payload = {"name": new_name}

        url = reverse(
            "cities-detail", args=[country_id, city_id]
        )  # FIXME add country_id to all these urls - POST "/api/cities/"
        response = admin_api_client_factory_boy.put(url, payload)

        assert response.status_code == HTTP_200_OK

        assert response.data["id"] == city_id
        assert response.data["name"] != old_name
        assert response.data["name"] == new_name

        city.refresh_from_db()

        assert city.name == new_name

    def test_update_city_by_regular_user_fails(self, user_api_client_factory_boy):
        city = CityFactory()
        country_id = str(city.country.id)
        city_id = str(city.id)
        old_name = city.name
        new_name = fake.city()
        payload = {"name": new_name}

        url = reverse(
            "cities-detail", args=[country_id, city_id]
        )  # FIXME add country_id to all these urls - POST "/api/cities/"
        response = user_api_client_factory_boy.put(url, payload)

        assert response.status_code == HTTP_403_FORBIDDEN
        assert str(response.data["detail"]) == "You do not have permission to perform this action."

        city = City.objects.get(id=city_id)
        assert str(city.id) == city_id
        assert city.name == old_name
        assert city.name != new_name

    def test_update_city_by_unauthenticated_admin_fails(self):
        city = CityFactory()
        country_id = str(city.country.id)
        city_id = str(city.id)
        old_name = city.name
        new_name = fake.city()
        payload = {"name": new_name}

        api_client = APIClient()
        url = reverse(
            "cities-detail", args=[country_id, city_id]
        )  # FIXME add country_id to all these urls - POST "/api/cities/"
        response = api_client.put(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == "Authentication credentials were not provided."

        city = City.objects.get(id=city_id)
        assert str(city.id) == city_id
        assert city.name == old_name
        assert city.name != new_name
