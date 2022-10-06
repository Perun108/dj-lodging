import random

import pytest
from django.utils import timezone
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APIClient

from djlodging.domain.lodgings.models.lodging import Lodging
from djlodging.domain.lodgings.repositories import LodgingRepository
from tests.domain.bookings.factories import BookingFactory
from tests.domain.lodgings.factories import CityFactory, LodgingFactory, ReviewFactory

fake = Faker()


@pytest.mark.django_db
class TestLodgingViewSet:
    def test_create_lodging_by_partner_succeeds(self, partner_api_client_pytest_fixture, partner):
        city = CityFactory()

        name = fake.word()
        kind = random.choice(Lodging.Type.choices)
        street = fake.street_name()
        house_number = fake.building_number()
        zip_code = fake.postcode()
        email = fake.email()
        phone_number = fake.phone_number()

        payload = {
            "name": name,
            "kind": kind,
            "city_id": str(city.id),
            "street": street,
            "house_number": house_number,
            "zip_code": zip_code,
            "email": email,
            "phone_number": phone_number,
            "price": 10,
        }

        url = reverse("lodgings-list")  # POST "/api/lodgings/"

        response = partner_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_201_CREATED

        lodging = Lodging.objects.first()
        assert lodging.name == name
        assert lodging.owner == partner
        assert lodging.kind == kind[1]
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
        kind = random.choice(Lodging.Type.choices)
        street = fake.street_name()
        house_number = fake.building_number()
        zip_code = fake.postcode()
        email = fake.email()
        phone_number = fake.phone_number()

        payload = {
            "name": name,
            "kind": kind,
            "city_id": str(city.id),
            "street": street,
            "house_number": house_number,
            "zip_code": zip_code,
            "email": email,
            "phone_number": phone_number,
            "price": 10,
        }

        url = reverse("lodgings-list")  # POST "/api/lodgings/"

        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_403_FORBIDDEN

    def test_list_available_succeeds_1(self, user_api_client_pytest_fixture):
        city = CityFactory()

        # Create 3 lodgings
        lodgings = LodgingFactory.create_batch(
            size=3, city=city, number_of_people=1, number_of_rooms=1
        )

        # The first date range is from today to tomorrow
        date_from1 = timezone.now().date()
        date_to1 = date_from1 + timezone.timedelta(days=1)

        # The second date range is from the day after tomorrow to 2 days after tomorrow
        date_from2 = timezone.now().date() + timezone.timedelta(days=1)
        date_to2 = date_from2 + timezone.timedelta(days=2)

        # Book two lodgings for these two date ranges - one lodging remains free
        BookingFactory(lodging=lodgings[0], date_from=date_from1, date_to=date_to1)
        BookingFactory(lodging=lodgings[1], date_from=date_from2, date_to=date_to2)

        query_params = {
            "city": city,
            "number_of_people": 1,
            "number_of_rooms": 1,
            # Check for availability for 7 days from today
            "date_from": date_from1,
            "date_to": date_from1 + timezone.timedelta(days=7),
            "available_only": True,
        }
        url = reverse("lodgings-list")
        response = user_api_client_pytest_fixture.get(url, query_params)

        assert response.status_code == HTTP_200_OK
        # We should have only 1 lodging available - the third one that has not been booked.
        assert len(response.data) == 1

    def test_list_available_succeeds_2(self, user_api_client_pytest_fixture):
        city = CityFactory()

        lodgings = LodgingFactory.create_batch(
            size=3, city=city, number_of_people=1, number_of_rooms=1
        )

        date_from1 = timezone.now().date()
        date_to1 = date_from1 + timezone.timedelta(days=1)

        date_from2 = timezone.now().date() + timezone.timedelta(days=1)
        date_to2 = date_from2 + timezone.timedelta(days=2)

        BookingFactory(lodging=lodgings[0], date_from=date_from1, date_to=date_to1)
        BookingFactory(lodging=lodgings[1], date_from=date_from2, date_to=date_to2)

        query_params = {
            "city": city,
            "number_of_people": 1,
            "number_of_rooms": 1,
            "date_from": date_from1 + timezone.timedelta(days=4),
            "date_to": date_from1 + timezone.timedelta(days=7),
            "available_only": True,
        }
        url = reverse("lodgings-list")
        response = user_api_client_pytest_fixture.get(url, query_params)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 3

    def test_list_available_succeeds_3(self, user_api_client_pytest_fixture):
        city = CityFactory()

        lodgings = LodgingFactory.create_batch(
            size=3, city=city, number_of_people=1, number_of_rooms=1
        )

        date_from1 = timezone.now().date()
        date_to1 = date_from1 + timezone.timedelta(days=1)

        date_from2 = timezone.now().date() + timezone.timedelta(days=1)
        date_to2 = date_from2 + timezone.timedelta(days=2)

        BookingFactory(lodging=lodgings[0], date_from=date_from1, date_to=date_to1)
        BookingFactory(lodging=lodgings[1], date_from=date_from2, date_to=date_to2)

        query_params = {
            "city": city,
            "number_of_people": 1,
            "number_of_rooms": 1,
            "date_from": date_from1,
            "date_to": date_from1 + timezone.timedelta(days=1),
            "available_only": True,
        }
        url = reverse("lodgings-list")
        response = user_api_client_pytest_fixture.get(url, query_params)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 2

    def test_list_available_succeeds_4(self, user_api_client_pytest_fixture):
        size = 3
        city = CityFactory()
        lodgings = LodgingFactory.create_batch(
            size=size, city=city, number_of_people=1, number_of_rooms=1
        )

        date_from = timezone.now().date()
        date_to = date_from + timezone.timedelta(days=1)

        for lodging in lodgings:
            BookingFactory(lodging=lodging, date_from=date_from, date_to=date_to)

        query_params = {
            "city": city,
            "number_of_people": 1,
            "number_of_rooms": 1,
            "date_from": date_from,
            "date_to": date_from + timezone.timedelta(days=1),
            "available_only": True,
        }
        url = reverse("lodgings-list")
        response = user_api_client_pytest_fixture.get(url, query_params)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 0

    def test_list_all_succeeds_1(self, user_api_client_pytest_fixture):
        size = 3
        city = CityFactory()
        lodgings = LodgingFactory.create_batch(
            size=size, city=city, number_of_people=1, number_of_rooms=1
        )

        date_from = timezone.now().date()
        date_to = date_from + timezone.timedelta(days=1)

        for lodging in lodgings:
            BookingFactory(lodging=lodging, date_from=date_from, date_to=date_to)

        query_params = {
            "city": city,
            "number_of_people": 1,
            "number_of_rooms": 1,
            "date_from": date_from,
            "date_to": date_from + timezone.timedelta(days=1),
        }
        url = reverse("lodgings-list")
        response = user_api_client_pytest_fixture.get(url, query_params)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == size

    def test_retrieve_succeeds(self, user_api_client_pytest_fixture):
        lodging = LodgingFactory()

        url = reverse("lodgings-detail", args=[str(lodging.id)])
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert response.data["id"] == str(lodging.id)

    def test_retrieve_by_unauthorized_user_fails(self):
        lodging = LodgingFactory()

        api_client = APIClient()

        url = reverse("lodgings-detail", args=[str(lodging.id)])
        response = api_client.get(url)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_average_rating_is_updated_after_new_review(self, user_api_client_pytest_fixture):
        lodging = LodgingFactory()

        # Assert that the newly created lodging has no rating since it has not reviews yet
        annotated_lodging = LodgingRepository.retrieve_lodging_with_average_rating(
            lodging_id=lodging.id
        )

        assert annotated_lodging.average_rating is None

        # Create reviews
        number_of_reviews = 3
        reviews = ReviewFactory.create_batch(lodging=lodging, size=number_of_reviews)

        # Calculate average rating for the lodging
        average_rating = sum([review.score for review in reviews]) / number_of_reviews

        url = reverse("lodgings-detail", args=[str(lodging.id)])
        response = user_api_client_pytest_fixture.get(url)

        # Response should contain 'average_rating' annotation equal to the one above
        assert response.data["average_rating"] == round(average_rating, ndigits=1)

        # Once again retrieve the lodging but this time it should have an 'average_rating'
        annotated_lodging = LodgingRepository.retrieve_lodging_with_average_rating(
            lodging_id=lodging.id
        )

        assert annotated_lodging.average_rating == round(average_rating, ndigits=1)
