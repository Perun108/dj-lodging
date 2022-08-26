import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import (  # HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APIClient

from djlodging.domain.lodgings.models import City
from tests.domain.lodgings.factories import CountryFactory

# from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestCityViewSet:
    def test_create_city_succeeds(self, admin_api_client_factory_boy):
        country = CountryFactory()
        name = fake.city()

        payload = {"country_id": str(country.id), "name": name}

        url = reverse("city-list")  # POST "/api/cities/"
        response = admin_api_client_factory_boy.post(url, payload)

        assert response.status_code == HTTP_201_CREATED

        city = City.objects.first()
        assert city is not None
        assert city.name == name

    def test_create_city_by_regular_user_fails(self, user_api_client_factory_boy):
        country = CountryFactory()
        name = fake.city()

        payload = {"country_id": str(country.id), "name": name}

        url = reverse("city-list")  # POST "/api/cities/"
        response = user_api_client_factory_boy.post(url, payload)

        assert response.status_code == HTTP_403_FORBIDDEN

        city = City.objects.first()
        assert city is None

    def test_create_city_without_country_fails(self, admin_api_client_factory_boy):
        name = fake.city()

        payload = {"country_id": "", "name": name}

        url = reverse("city-list")  # POST "/api/cities/"
        response = admin_api_client_factory_boy.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'country_id': [ErrorDetail(string='Must be a valid UUID.', code='invalid')]}"
        )

        city = City.objects.first()
        assert city is None

    def test_create_city_by_unauthenticated_admin_fails(self):
        api_client = APIClient()

        country = CountryFactory()
        name = fake.city()

        payload = {"country_id": str(country.id), "name": name}

        url = reverse("city-list")  # POST "/api/cities/"
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED

        city = City.objects.first()
        assert city is None
