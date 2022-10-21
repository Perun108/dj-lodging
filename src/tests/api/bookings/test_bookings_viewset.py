import pytest
from faker import Faker
from pytest_django.asserts import assertQuerysetEqual
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from djlodging.domain.bookings.models import Booking
from tests.domain.bookings.factories import BookingFactory
from tests.domain.lodgings.factories import LodgingFactory
from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestBookingViewSet:
    def test_list_all_with_multiple_booked_lodgings_succeeds(
        self, admin_api_client_pytest_fixture
    ):
        user_1 = UserFactory()
        user_2 = UserFactory()

        lodging_1 = LodgingFactory()
        lodging_2 = LodgingFactory()

        bookings_count_1 = 3
        bookings_count_2 = 2

        assert Booking.objects.count() == 0

        bookings_for_lodging_1 = BookingFactory.create_batch(
            size=bookings_count_1, user=user_1, lodging=lodging_1
        )
        bookings_for_lodging_2 = BookingFactory.create_batch(
            size=bookings_count_2, user=user_2, lodging=lodging_2
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == bookings_count_1 + bookings_count_2
        assert Booking.objects.count() == bookings_count_1 + bookings_count_2
        assertQuerysetEqual(
            Booking.objects.all(), bookings_for_lodging_1 + bookings_for_lodging_2, ordered=False
        )

    def test_list_all_without_bookings_succeeds(self, admin_api_client_pytest_fixture):
        assert Booking.objects.count() == 0

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 0
        assert Booking.objects.count() == 0

    def test_list_all_by_non_admin_fails(self, user_api_client_pytest_fixture):
        user = UserFactory()
        lodging = LodgingFactory()
        bookings_count = 3

        assert Booking.objects.count() == 0

        BookingFactory.create_batch(size=bookings_count, user=user, lodging=lodging)

        url = reverse("bookings-list")
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_403_FORBIDDEN

    def test_retrieve_succeeds(self, admin_api_client_pytest_fixture):
        assert Booking.objects.count() == 0

        booking = BookingFactory()
        booking_id = str(booking.id)

        url = reverse("bookings-detail", args=[booking_id])
        response = admin_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert response.data["id"] == booking_id

    def test_retrieve_by_non_admin_fails(self, user_api_client_pytest_fixture):
        assert Booking.objects.count() == 0

        booking = BookingFactory()
        booking_id = str(booking.id)

        url = reverse("bookings-detail", args=[booking_id])
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_403_FORBIDDEN
