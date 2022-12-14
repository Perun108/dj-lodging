import pytest
from django.utils import timezone
from faker import Faker
from pytest_django.asserts import assertQuerysetEqual
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)

from djlodging.domain.bookings.models import Booking
from djlodging.infrastructure.providers.payments import payment_provider
from tests.domain.bookings.factories import BookingFactory
from tests.domain.lodgings.factories import LodgingFactory
from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestMyBookingViewSet:
    def test_create_succeeds(self, user_api_client_pytest_fixture, user):
        lodging = LodgingFactory()
        date_from = timezone.now().date() + timezone.timedelta(days=1)
        date_to = date_from + timezone.timedelta(days=2)

        payload = {
            "lodging_id": lodging.id,
            "date_from": date_from,
            "date_to": date_to,
        }
        url = reverse("my-bookings-list")
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
        url = reverse("my-bookings-list")
        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["message"] == "The dates are invalid"

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
        url = reverse("my-bookings-list")
        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Date_to must be greater than date_from"

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
        url = reverse("my-bookings-list")
        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Date_to must be greater than date_from"

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
        url = reverse("my-bookings-list")
        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Date_to must be greater than date_from"

        booking = Booking.objects.first()
        assert booking is None

    def test_list_for_multiple_lodgings_succeeds(self, user_api_client_pytest_fixture, user):
        bookings_number_1 = 3
        bookings_number_2 = 2

        assert Booking.objects.count() == 0

        lodging_1 = LodgingFactory()
        lodging_2 = LodgingFactory()

        bookings_for_lodging_1 = BookingFactory.create_batch(
            size=bookings_number_1, user=user, lodging=lodging_1
        )
        bookings_for_lodging_2 = BookingFactory.create_batch(
            size=bookings_number_2, user=user, lodging=lodging_2
        )

        url = reverse("my-bookings-list")
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert (
            response.data["count"]
            == bookings_number_1 + bookings_number_2
            == Booking.objects.count()
        )
        assertQuerysetEqual(
            Booking.objects.all(), bookings_for_lodging_1 + bookings_for_lodging_2, ordered=False
        )

    def test_list_for_multiple_lodgings_with_other_users_reviews_succeeds(
        self, user_api_client_pytest_fixture, user
    ):
        another_user = UserFactory()
        another_user_bookings_number = 4

        bookings_number_1 = 3
        bookings_number_2 = 2

        assert Booking.objects.count() == 0
        lodging_1 = LodgingFactory()
        lodging_2 = LodgingFactory()

        BookingFactory.create_batch(size=bookings_number_1, user=user, lodging=lodging_1)
        BookingFactory.create_batch(size=bookings_number_2, user=user, lodging=lodging_2)
        BookingFactory.create_batch(
            size=another_user_bookings_number, user=another_user, lodging=lodging_1
        )

        url = reverse("my-bookings-list")
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert response.data["count"] == bookings_number_1 + bookings_number_2
        assert (
            Booking.objects.count()
            == bookings_number_1 + bookings_number_2 + another_user_bookings_number
        )

    def test_list_for_single_lodging_succeeds(self, user_api_client_pytest_fixture, user):
        bookings_number = 3

        assert Booking.objects.count() == 0

        bookings = BookingFactory.create_batch(size=bookings_number, user=user)

        url = reverse("my-bookings-list")
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert response.data["count"] == bookings_number == Booking.objects.count()
        assertQuerysetEqual(Booking.objects.all(), bookings, ordered=False)

    def test_list_for_single_lodging_with_other_users_bookings_succeeds(
        self, user_api_client_pytest_fixture, user
    ):
        another_user = UserFactory()
        another_user_bookings_number = 4

        bookings_number = 3

        assert Booking.objects.count() == 0

        BookingFactory.create_batch(size=bookings_number, user=user)
        BookingFactory.create_batch(size=another_user_bookings_number, user=another_user)

        url = reverse("my-bookings-list")
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert response.data["count"] == bookings_number
        assert Booking.objects.count() == bookings_number + another_user_bookings_number

    def test_list_without_my_bookings_succeeds(self, user_api_client_pytest_fixture, user):
        another_user = UserFactory()
        BookingFactory(user=another_user)

        assert Booking.objects.count() == 1

        url = reverse("my-bookings-list")
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert response.data["count"] == 0
        assert Booking.objects.count() == 1

    def test_pay_succeeds(self, user_with_payment_api_client_pytest_fixture, user_with_payment):
        booking = BookingFactory(user=user_with_payment)
        payload = {}
        url = reverse("my-bookings-pay", args=[str(booking.id)])
        response = user_with_payment_api_client_pytest_fixture.post(url, payload, format="json")
        assert response.status_code == HTTP_201_CREATED
        assert "client_secret" in response.data
        assert response.data["client_secret"].startswith("pi_") is True
        assert "_secret_" in response.data["client_secret"]

        ind = response.data["client_secret"].index("_secret_")
        payment_intent_id = response.data["client_secret"][:ind]
        payment_intent = payment_provider.get_payment_intent(payment_intent_id)

        assert int(payment_intent.amount / 100) == int(booking.lodging.price)
        assert payment_intent.client_secret == response.data["client_secret"]
        assert payment_intent["metadata"] == {"booking_id": str(booking.id)}
        assert payment_intent.payment_method is None
        assert payment_intent.status == "requires_payment_method"

        booking.refresh_from_db()
        assert booking.payment_intent_id == payment_intent_id

    def test_pay_by_another_user_fails(self, user_api_client_pytest_fixture, user):
        booking = BookingFactory()

        payload = {}
        url = reverse("my-bookings-pay", args=[str(booking.id)])
        response = user_api_client_pytest_fixture.post(url, payload, format="json")

        assert response.status_code == HTTP_403_FORBIDDEN
        assert str(response.data["detail"]) == "You do not have permission to perform this action."

        booking.refresh_from_db()
        assert booking.payment_intent_id == ""

        # NOTE: .cancel API cannot be integration-tested properly since it would require:
        # creating a real payment intent, attaching a payment method to it and confirming it.
        # This cannot be done programmatically.
