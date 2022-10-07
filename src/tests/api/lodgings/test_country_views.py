from uuid import uuid4

import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APIClient

from djlodging.domain.lodgings.models import Country
from tests.domain.lodgings.factories import CountryFactory

# from tests.domain.lodgings.factories import CountryFactory

# from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestCountryViewSet:
    def test_create_country_by_admin_succeeds(self, admin_api_client_factory_boy):
        name = fake.country()
        payload = {"name": name}
        url = reverse("countries-list")  # POST "/api/countries/"

        response = admin_api_client_factory_boy.post(url, payload)
        assert response.status_code == HTTP_201_CREATED

        country = Country.objects.first()
        assert country.name == name

    def test_create_country_by_regular_user_fails(self, user_api_client_factory_boy):
        name = fake.country()
        payload = {"name": name}
        url = reverse("countries-list")  # POST "/api/countries/"

        response = user_api_client_factory_boy.post(url, payload)
        assert response.status_code == HTTP_403_FORBIDDEN

        country = Country.objects.first()
        assert country is None

    def test_create_country_by_unauthenticated_admin_fails(self):
        api_client = APIClient()

        name = fake.country()
        payload = {"name": name}
        url = reverse("countries-list")  # POST "/api/countries/"

        response = api_client.post(url, payload)
        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert (
            str(response.data)
            == "{'detail': ErrorDetail(string='Authentication credentials were not provided.', "
            "code='not_authenticated')}"
        )

        country = Country.objects.first()
        assert country is None

    def test_create_country_without_name_fails(self, admin_api_client_factory_boy):
        payload = {"name": ""}
        url = reverse("countries-list")  # "/api/countries/country-list/"
        response = admin_api_client_factory_boy.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'name': [ErrorDetail(string='This field may not be blank.', code='blank')]}"
        )

    def test_retrieve_country_by_admin_succeeds(self, admin_api_client_factory_boy):
        country = CountryFactory()

        url = reverse(
            "countries-detail", args=[str(country.id)]
        )  # GET "/api/countries/{country_id}"

        response = admin_api_client_factory_boy.get(url)

        assert response.status_code == HTTP_200_OK
        assert response.data["id"] == str(country.id)
        assert response.data["name"] == str(country.name)

    def test_retrieve_country_by_regular_user_fails(self, user_api_client_factory_boy):
        country = CountryFactory()

        url = reverse(
            "countries-detail", args=[str(country.id)]
        )  # GET "/api/countries/{country_id}"

        response = user_api_client_factory_boy.post(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_retrieve_country_by_unauthenticated_admin_fails(self):
        api_client = APIClient()
        country = CountryFactory()

        url = reverse(
            "countries-detail", args=[str(country.id)]
        )  # GET "/api/countries/{country_id}"

        response = api_client.post(url)
        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert (
            str(response.data)
            == "{'detail': ErrorDetail(string='Authentication credentials were not provided.', "
            "code='not_authenticated')}"
        )

    def test_retrieve_country_with_wrong_id_fails(self, admin_api_client_factory_boy):
        correct_id = uuid4()
        CountryFactory(id=correct_id)
        wrong_id = uuid4()

        url = reverse(
            "countries-detail", args=[str(wrong_id)]
        )  # GET "/api/countries/{country_id}"

        response = admin_api_client_factory_boy.get(url)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data) == "{'detail': {'non_field_errors': "
            "[ErrorDetail(string='There is no country with this id', code='invalid')]}}"
        )

    def test_list_countries_by_admin_succeeds(self, admin_api_client_factory_boy):
        number_of_countries = 3
        CountryFactory.create_batch(size=number_of_countries)

        url = reverse("countries-list")  # GET "/api/countries/"

        response = admin_api_client_factory_boy.get(url)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == number_of_countries

    def test_list_countries_by_regular_user_fails(self, user_api_client_factory_boy):
        number_of_countries = 3
        CountryFactory.create_batch(size=number_of_countries)

        url = reverse("countries-list")  # GET "/api/countries/"
        response = user_api_client_factory_boy.post(url)

        assert response.status_code == HTTP_403_FORBIDDEN

    def test_list_countries_by_unauthenticated_admin_fails(self):
        api_client = APIClient()

        number_of_countries = 3
        CountryFactory.create_batch(size=number_of_countries)
        url = reverse("countries-list")  # GET "/api/countries/"

        response = api_client.post(url)
        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert (
            str(response.data)
            == "{'detail': ErrorDetail(string='Authentication credentials were not provided.', "
            "code='not_authenticated')}"
        )

    def test_update_country_by_admin_succeeds(self, admin_api_client_factory_boy):
        old_name = fake.country()
        country = CountryFactory(name=old_name)
        new_name = fake.country()

        payload = {"name": new_name}
        url = reverse(
            "countries-detail", args=[str(country.id)]
        )  # PUT "/api/countries/{country_id}"

        response = admin_api_client_factory_boy.put(url, payload)

        assert response.status_code == HTTP_200_OK
        assert response.data["id"] == str(country.id)
        assert response.data["name"] == new_name

    def test_update_country_by_unauthenticated_admin_fails(self):
        api_client = APIClient()
        old_name = fake.country()
        country = CountryFactory(name=old_name)
        new_name = fake.country()

        payload = {"name": new_name}
        url = reverse(
            "countries-detail", args=[str(country.id)]
        )  # PUT "/api/countries/{country_id}"

        response = api_client.put(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_update_country_by_regular_user_fails(self, user_api_client_factory_boy):
        old_name = fake.country()
        country = CountryFactory(name=old_name)
        new_name = fake.country()

        payload = {"name": new_name}
        url = reverse(
            "countries-detail", args=[str(country.id)]
        )  # PUT "/api/countries/{country_id}"

        response = user_api_client_factory_boy.put(url, payload)

        assert response.status_code == HTTP_403_FORBIDDEN

    def test_update_country_with_wrong_id_fails(self, admin_api_client_factory_boy):
        old_name = fake.country()
        new_name = fake.country()
        correct_id = uuid4()
        wrong_id = uuid4()
        CountryFactory(id=correct_id, name=old_name)

        payload = {"name": new_name}
        url = reverse("countries-detail", args=[wrong_id])  # PUT "/api/countries/{country_id}"

        response = admin_api_client_factory_boy.put(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data) == "{'detail': {'non_field_errors': "
            "[ErrorDetail(string='There is no country with this id', code='invalid')]}}"
        )

    def test_delete_country_by_admin_succeeds(self, admin_api_client_factory_boy):
        country = CountryFactory()

        db_country = Country.objects.first()
        assert db_country is not None
        assert db_country == country

        url = reverse(
            "countries-detail", args=[str(country.id)]
        )  # DELETE "/api/countries/{country_id}"

        response = admin_api_client_factory_boy.delete(url)

        assert response.status_code == HTTP_204_NO_CONTENT
        assert Country.objects.first() is None

    def test_delete_country_by_unauthenticated_admin_fails(self):
        api_client = APIClient()
        country = CountryFactory()

        url = reverse(
            "countries-detail", args=[str(country.id)]
        )  # DELETE "/api/countries/{country_id}"

        response = api_client.delete(url)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_delete_country_by_regular_user_fails(self, user_api_client_factory_boy):
        country = CountryFactory()

        url = reverse(
            "countries-detail", args=[str(country.id)]
        )  # DELETE "/api/countries/{country_id}"

        response = user_api_client_factory_boy.delete(url)

        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_country_with_wrong_id_fails(self, admin_api_client_factory_boy):
        correct_id = uuid4()
        wrong_id = uuid4()
        CountryFactory(id=correct_id)

        url = reverse("countries-detail", args=[wrong_id])  # DELETE "/api/countries/{country_id}"

        response = admin_api_client_factory_boy.delete(url)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data) == "{'detail': {'non_field_errors': "
            "[ErrorDetail(string='There is no country with this id', code='invalid')]}}"
        )
