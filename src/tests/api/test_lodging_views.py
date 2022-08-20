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

from djlodging.domain.lodgings.models import City, Country  # , Lodging, LodgingImage
from tests.domain.lodgings.factories import CountryFactory

# from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestCountryViewSet:
    def test_create_country_by_admin_succeeds(self, admin_api_client):
        name = fake.country()
        payload = {"name": name}
        url = reverse("country-list")  # POST "/api/countries/"

        response = admin_api_client.post(url, payload)
        assert response.status_code == HTTP_201_CREATED

        country = Country.objects.first()
        assert country.name == name

    def test_create_country_by_regular_user_fails(self, user_api_client):
        name = fake.country()
        payload = {"name": name}
        url = reverse("country-list")  # POST "/api/countries/"

        response = user_api_client.post(url, payload)
        assert response.status_code == HTTP_403_FORBIDDEN

        country = Country.objects.first()
        assert country is None

    def test_create_country_by_unauthenticated_admin_fails(self):
        api_client = APIClient()

        name = fake.country()
        payload = {"name": name}
        url = reverse("country-list")  # POST "/api/countries/"

        response = api_client.post(url, payload)
        assert response.status_code == HTTP_401_UNAUTHORIZED

        country = Country.objects.first()
        assert country is None

    def test_country_without_name_fails(self, admin_api_client):
        payload = {"name": ""}
        url = reverse("country-list")  # "/api/countries/country-list/"
        response = admin_api_client.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'name': [ErrorDetail(string='This field may not be blank.', code='blank')]}"
        )


@pytest.mark.django_db
class TestCityViewSet:
    def test_create_city_succeeds(self, admin_api_client):
        country = CountryFactory()
        name = fake.city()

        payload = {"country_id": str(country.id), "name": name}

        url = reverse("city-list")  # POST "/api/cities/"
        response = admin_api_client.post(url, payload)

        assert response.status_code == HTTP_201_CREATED

        city = City.objects.first()
        assert city is not None
        assert city.name == name

    def test_create_city_by_regular_user_fails(self, user_api_client):
        country = CountryFactory()
        name = fake.city()

        payload = {"country_id": str(country.id), "name": name}

        url = reverse("city-list")  # POST "/api/cities/"
        response = user_api_client.post(url, payload)

        assert response.status_code == HTTP_403_FORBIDDEN

        city = City.objects.first()
        assert city is None

    def test_create_city_without_country_fails(self, admin_api_client):
        name = fake.city()

        payload = {"country_id": "", "name": name}

        url = reverse("city-list")  # POST "/api/cities/"
        response = admin_api_client.post(url, payload)

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
