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

from djlodging.domain.lodgings.models import Country

# from tests.domain.lodgings.factories import CountryFactory

# from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestCountryViewSet:
    def test_create_country_by_admin_succeeds(self, admin_api_client_factory_boy):
        name = fake.country()
        payload = {"name": name}
        url = reverse("country-list")  # POST "/api/countries/"

        response = admin_api_client_factory_boy.post(url, payload)
        assert response.status_code == HTTP_201_CREATED

        country = Country.objects.first()
        assert country.name == name

    def test_create_country_by_regular_user_fails(self, user_api_client_factory_boy):
        name = fake.country()
        payload = {"name": name}
        url = reverse("country-list")  # POST "/api/countries/"

        response = user_api_client_factory_boy.post(url, payload)
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
        assert (
            str(response.data)
            == "{'detail': ErrorDetail(string='Authentication credentials were not provided.', "
            "code='not_authenticated')}"
        )

        country = Country.objects.first()
        assert country is None

    def test_country_without_name_fails(self, admin_api_client_factory_boy):
        payload = {"name": ""}
        url = reverse("country-list")  # "/api/countries/country-list/"
        response = admin_api_client_factory_boy.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'name': [ErrorDetail(string='This field may not be blank.', code='blank')]}"
        )
