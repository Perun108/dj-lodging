import random

import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import (  # HTTP_200_OK,; HTTP_400_BAD_REQUEST,; HTTP_401_UNAUTHORIZED,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
)

from djlodging.domain.lodgings.models.lodging import Lodging
from tests.domain.lodgings.factories import CityFactory

fake = Faker()


@pytest.mark.django_db
class TestLodgingViewSet:
    def test_create_lodging_by_partner_succeeds(self, partner_api_client_pytest_fixture, partner):
        city = CityFactory()

        name = fake.word()
        type = random.choice(Lodging.Type.choices)
        street = fake.street_name()
        house_number = fake.building_number()
        zip_code = fake.postcode()
        email = fake.email()
        phone_number = fake.phone_number()

        payload = {
            "name": name,
            "type": type,
            "city_id": str(city.id),
            "street": street,
            "house_number": house_number,
            "zip_code": zip_code,
            "email": email,
            "phone_number": phone_number,
        }

        url = reverse("lodging-list")  # POST "/api/lodgings/"

        response = partner_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_201_CREATED

        lodging = Lodging.objects.first()
        assert lodging.name == name
        assert lodging.owner == partner
        assert lodging.type == type[1]
        assert lodging.city == city
        assert lodging.street == street
        assert lodging.house_number == house_number
        assert lodging.zip_code == zip_code
        assert lodging.email == email
        assert lodging.phone_number == phone_number

    def test_create_lodging_by_non_partner_fails(self, user_api_client_pytest_fixture):
        city = CityFactory()

        name = fake.word()
        type = random.choice(Lodging.Type.choices)
        street = fake.street_name()
        house_number = fake.building_number()
        zip_code = fake.postcode()
        email = fake.email()
        phone_number = fake.phone_number()

        payload = {
            "name": name,
            "type": type,
            "city_id": str(city.id),
            "street": street,
            "house_number": house_number,
            "zip_code": zip_code,
            "email": email,
            "phone_number": phone_number,
        }

        url = reverse("lodging-list")  # POST "/api/lodgings/"

        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_403_FORBIDDEN
