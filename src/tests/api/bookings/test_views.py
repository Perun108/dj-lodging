import pytest
from django.utils import timezone
from faker import Faker
from pytest_django.asserts import assertQuerysetEqual
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from djlodging.domain.bookings.models import Booking
from tests.domain.bookings.factories import BookingFactory
from tests.domain.lodgings.factories import LodgingFactory

fake = Faker()


@pytest.mark.django_db
class TestBookingViewSet:
    def test_create_succeeds(self, user_api_client_pytest_fixture, user):
        lodging = LodgingFactory()
        date_from = timezone.now().date() + timezone.timedelta(days=1)
        date_to = date_from + timezone.timedelta(days=2)

        payload = {
            "lodging_id": lodging.id,
            "date_from": date_from,
            "date_to": date_to,
        }
        url = reverse("booking-list")
        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_201_CREATED
        assert response.data["user_id"] == str(user.id)
        assert response.data["date_from"] == str(date_from)
        assert response.data["date_to"] == str(date_to)
        assert response.data["lodging"]["id"] == str(lodging.id)
        assert response.data["status"] == Booking.Status.PAYMENT_PENDING

    def test_create_booking_with_invalid_date_from_fails(
        self, user_api_client_pytest_fixture, user
    ):
        lodging = LodgingFactory()
        date_from = timezone.now().date() - timezone.timedelta(days=1)
        date_to = date_from + timezone.timedelta(days=2)

        payload = {
            "lodging_id": lodging.id,
            "date_from": date_from,
            "date_to": date_to,
        }
        url = reverse("booking-list")
        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'non_field_errors': [ErrorDetail(string='The dates are invalid', code='invalid')]}"  # noqa
        )

        booking = Booking.objects.first()
        assert booking is None

    def test_create_booking_with_invalid_date_to_fails(self, user_api_client_pytest_fixture, user):
        lodging = LodgingFactory()
        date_from = timezone.now().date() + timezone.timedelta(days=1)
        date_to = date_from - timezone.timedelta(days=2)

        payload = {
            "lodging_id": lodging.id,
            "date_from": date_from,
            "date_to": date_to,
        }
        url = reverse("booking-list")
        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'non_field_errors': [ErrorDetail(string='The dates are invalid', code='invalid')]}"  # noqa
        )

        booking = Booking.objects.first()
        assert booking is None

    def test_create_booking_with_equal_dates_fails(self, user_api_client_pytest_fixture, user):
        lodging = LodgingFactory()
        date_from = timezone.now().date() - timezone.timedelta(days=1)
        date_to = date_from

        payload = {
            "lodging_id": lodging.id,
            "date_from": date_from,
            "date_to": date_to,
        }
        url = reverse("booking-list")
        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'non_field_errors': [ErrorDetail(string='Please provide date_to', code='invalid')]}"  # noqa
        )

        booking = Booking.objects.first()
        assert booking is None

    def test_create_booking_with_date_from_greater_than_date_to_fails(
        self, user_api_client_pytest_fixture, user
    ):
        lodging = LodgingFactory()
        date_from = timezone.now().date() + timezone.timedelta(days=2)
        date_to = timezone.now().date()

        payload = {
            "lodging_id": lodging.id,
            "date_from": date_from,
            "date_to": date_to,
        }
        url = reverse("booking-list")
        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'non_field_errors': [ErrorDetail(string='The dates are invalid', code='invalid')]}"  # noqa
        )

        booking = Booking.objects.first()
        assert booking is None

    def test_list_succeeds(self, user_api_client_pytest_fixture, user):
        count = 3
        assert Booking.objects.count() == 0

        bookings = BookingFactory.create_batch(size=count, user=user)
        url = reverse("booking-list")
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == count
        assert Booking.objects.count() == count
        assertQuerysetEqual(Booking.objects.all(), bookings, ordered=False)
