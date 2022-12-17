import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from rest_framework.test import APIClient

from djlodging.domain.lodgings.models import City
from tests.domain.lodgings.factories import CountryFactory

fake = Faker()


@pytest.mark.django_db
class TestCreateCity:
    def test_create_city_succeeds(self, admin_api_client_factory_boy):
        country = CountryFactory()
        name = fake.city()

        payload = {"name": name}

        url = reverse("cities-list", args=[str(country.id)])  # POST "/api/cities/"
        response = admin_api_client_factory_boy.post(url, payload)

        assert response.status_code == HTTP_201_CREATED

        city = City.objects.first()
        assert city is not None
        assert city.name == name
        assert city.country.id == country.id

    def test_create_city_by_regular_user_fails(self, user_api_client_factory_boy):
        country = CountryFactory()
        name = fake.city()

        payload = {"name": name}

        url = reverse("cities-list", args=[str(country.id)])  # POST "/api/cities/"
        response = user_api_client_factory_boy.post(url, payload)

        assert response.status_code == HTTP_403_FORBIDDEN
        assert str(response.data["detail"]) == "You do not have permission to perform this action."

        city = City.objects.first()
        assert city is None

    def test_create_city_by_unauthenticated_admin_fails(self):
        api_client = APIClient()

        country = CountryFactory()
        name = fake.city()

        payload = {"name": name}

        url = reverse("cities-list", args=[str(country.id)])  # POST "/api/cities/"
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == "Authentication credentials were not provided."

        city = City.objects.first()
        assert city is None
