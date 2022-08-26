import random

import pytest
from django.utils import timezone
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN

from djlodging.domain.lodgings.models.lodging import Lodging
from tests.domain.bookings.factories import BookingFactory
from tests.domain.lodgings.factories import CityFactory, LodgingFactory

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
            "price": 10,
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
        assert lodging.price == 10

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
            "price": 10,
        }

        url = reverse("lodging-list")  # POST "/api/lodgings/"

        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_403_FORBIDDEN

    def test_list_available_succeeds(self, user_api_client_pytest_fixture):
        city = CityFactory()

        lodging1 = LodgingFactory(city=city, number_of_people=1, number_of_rooms=1)
        lodging2 = LodgingFactory(city=city, number_of_people=1, number_of_rooms=1)
        lodging3 = LodgingFactory(city=city, number_of_people=1, number_of_rooms=1)  # noqa

        date_from1 = timezone.now().date()
        date_to1 = date_from1 + timezone.timedelta(days=1)

        date_from2 = timezone.now().date() + timezone.timedelta(days=1)
        date_to2 = date_from2 + timezone.timedelta(days=2)

        booking1 = BookingFactory(lodging=lodging1, date_from=date_from1, date_to=date_to1)  # noqa
        booking2 = BookingFactory(lodging=lodging2, date_from=date_from2, date_to=date_to2)  # noqa

        query_params = {
            "city": city,
            "number_of_people": 1,
            "number_of_rooms": 1,
            "date_from": date_from1,
            "date_to": date_from1 + timezone.timedelta(days=7),
        }
        url = reverse("lodging-list-available")
        response = user_api_client_pytest_fixture.get(url, query_params)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 1

    def test_list_available_succeeds_2(self, user_api_client_pytest_fixture):
        city = CityFactory()

        lodging1 = LodgingFactory(city=city, number_of_people=1, number_of_rooms=1)
        lodging2 = LodgingFactory(city=city, number_of_people=1, number_of_rooms=1)
        lodging3 = LodgingFactory(city=city, number_of_people=1, number_of_rooms=1)  # noqa

        date_from1 = timezone.now().date()
        date_to1 = date_from1 + timezone.timedelta(days=1)

        date_from2 = timezone.now().date() + timezone.timedelta(days=1)
        date_to2 = date_from2 + timezone.timedelta(days=2)

        booking1 = BookingFactory(lodging=lodging1, date_from=date_from1, date_to=date_to1)  # noqa
        booking2 = BookingFactory(lodging=lodging2, date_from=date_from2, date_to=date_to2)  # noqa

        query_params = {
            "city": city,
            "number_of_people": 1,
            "number_of_rooms": 1,
            "date_from": date_from1 + timezone.timedelta(days=4),
            "date_to": date_from1 + timezone.timedelta(days=7),
        }
        url = reverse("lodging-list-available")
        response = user_api_client_pytest_fixture.get(url, query_params)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 3

    def test_list_available_succeeds_3(self, user_api_client_pytest_fixture):
        city = CityFactory()

        lodging1 = LodgingFactory(city=city, number_of_people=1, number_of_rooms=1)
        lodging2 = LodgingFactory(city=city, number_of_people=1, number_of_rooms=1)
        lodging3 = LodgingFactory(city=city, number_of_people=1, number_of_rooms=1)  # noqa

        date_from1 = timezone.now().date()
        date_to1 = date_from1 + timezone.timedelta(days=1)

        date_from2 = timezone.now().date() + timezone.timedelta(days=1)
        date_to2 = date_from2 + timezone.timedelta(days=2)

        booking1 = BookingFactory(lodging=lodging1, date_from=date_from1, date_to=date_to1)  # noqa
        booking2 = BookingFactory(lodging=lodging2, date_from=date_from2, date_to=date_to2)  # noqa

        query_params = {
            "city": city,
            "number_of_people": 1,
            "number_of_rooms": 1,
            "date_from": date_from1,
            "date_to": date_from1 + timezone.timedelta(days=1),
        }
        url = reverse("lodging-list-available")
        response = user_api_client_pytest_fixture.get(url, query_params)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 2

    def test_list_available_succeeds_4(self, user_api_client_pytest_fixture):
        city = CityFactory()

        lodging1 = LodgingFactory(city=city, number_of_people=1, number_of_rooms=1)
        lodging2 = LodgingFactory(city=city, number_of_people=1, number_of_rooms=1)
        lodging3 = LodgingFactory(city=city, number_of_people=1, number_of_rooms=1)

        date_from1 = timezone.now().date()
        date_to1 = date_from1 + timezone.timedelta(days=1)

        date_from2 = timezone.now().date() + timezone.timedelta(days=1)
        date_to2 = date_from2 + timezone.timedelta(days=2)  # noqa

        booking1 = BookingFactory(lodging=lodging1, date_from=date_from1, date_to=date_to1)  # noqa
        booking2 = BookingFactory(lodging=lodging2, date_from=date_from1, date_to=date_to1)  # noqa
        booking2 = BookingFactory(lodging=lodging3, date_from=date_from1, date_to=date_to1)  # noqa

        query_params = {
            "city": city,
            "number_of_people": 1,
            "number_of_rooms": 1,
            "date_from": date_from1,
            "date_to": date_from1 + timezone.timedelta(days=1),
        }
        url = reverse("lodging-list-available")
        response = user_api_client_pytest_fixture.get(url, query_params)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 0
