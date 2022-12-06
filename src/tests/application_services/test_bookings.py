import pytest
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from faker import Faker

from djlodging.application_services.bookings import BookingService
from djlodging.domain.bookings.models import Booking
from djlodging.domain.core.base_exceptions import DjLodgingValidationError
from tests.domain.bookings.factories import BookingFactory
from tests.domain.lodgings.factories import LodgingFactory
from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestBookingService:
    def test_create_booking_succeeds(self):
        lodging = LodgingFactory()
        user = UserFactory()
        date_from = timezone.now().date() + timezone.timedelta(days=1)
        date_to = date_from + timezone.timedelta(days=2)

        booking = BookingService.create(
            lodging_id=lodging.id, user=user, date_from=date_from, date_to=date_to
        )

        assert booking is not None
        assert booking == Booking.objects.first()
        assert booking.lodging == lodging
        assert booking.user == user
        assert booking.date_from == date_from
        assert booking.date_to == date_to

    def test_create_booking_with_invalid_date_from_fails(self):
        lodging = LodgingFactory()
        user = UserFactory()
        date_from = timezone.now().date() - timezone.timedelta(days=1)
        date_to = date_from + timezone.timedelta(days=2)

        with pytest.raises(DjLodgingValidationError) as exc:
            BookingService.create(
                lodging_id=lodging.id, user=user, date_from=date_from, date_to=date_to
            )
        assert str(exc.value) == "The dates are invalid"

        booking = Booking.objects.first()
        assert booking is None

    def test_create_booking_with_invalid_date_to_fails(self):
        lodging = LodgingFactory()
        user = UserFactory()
        date_from = timezone.now().date() + timezone.timedelta(days=1)
        date_to = date_from - timezone.timedelta(days=2)

        with pytest.raises(DjLodgingValidationError) as exc:
            BookingService.create(
                lodging_id=lodging.id, user=user, date_from=date_from, date_to=date_to
            )
        assert str(exc.value) == "Date_to must be greater than date_from"

        booking = Booking.objects.first()
        assert booking is None

    def test_create_booking_with_equal_dates_fails(self):
        lodging = LodgingFactory()
        user = UserFactory()
        date_from = timezone.now().date() - timezone.timedelta(days=1)
        date_to = date_from

        with pytest.raises(DjLodgingValidationError) as exc:
            BookingService.create(
                lodging_id=lodging.id, user=user, date_from=date_from, date_to=date_to
            )
        assert str(exc.value) == "Date_to must be greater than date_from"

        booking = Booking.objects.first()
        assert booking is None

    def test_create_booking_with_date_from_greater_than_date_to_fails(self):
        lodging = LodgingFactory()
        user = UserFactory()
        date_from = timezone.now().date() + timezone.timedelta(days=2)
        date_to = timezone.now().date()

        with pytest.raises(DjLodgingValidationError) as exc:
            BookingService.create(
                lodging_id=lodging.id, user=user, date_from=date_from, date_to=date_to
            )
        assert str(exc.value) == "Date_to must be greater than date_from"

        booking = Booking.objects.first()
        assert booking is None

    def test_pay_succeeds(self, mocker):
        user = UserFactory()
        booking = BookingFactory(user=user)

        assert booking.status == Booking.Status.PAYMENT_PENDING

        mock_payment_intent = mocker.patch(
            "djlodging.application_services.payments.PaymentService.create_payment"
        )

        mock_id = fake.word()
        mock_client_secret = fake.word()
        mock_payment_intent.return_value.id = mock_id
        mock_payment_intent.return_value.client_secret = mock_client_secret

        client_secret = BookingService.pay(actor=user, booking_id=booking.id)
        mock_payment_intent.assert_called_once()

        assert client_secret == mock_client_secret

        booking.refresh_from_db()

        assert booking.payment_intent_id == mock_id
        # NOTE:
        # We can't test for booking.status == Booking.Status.PAID as that requires a webhook event.

    def test_cancel_succeeds(self, mocker):
        user = UserFactory()
        booking = BookingFactory(user=user, status=Booking.Status.PAID)

        mock = mocker.patch(
            "djlodging.application_services.payments.PaymentService.create_refund",
            return_value=None,
        )
        canceled_booking = BookingService.cancel(actor=user, booking_id=booking.id)
        mock.assert_called_once()
        assert canceled_booking.status == Booking.Status.CANCELED

    def test_cancel_booking_with_wrong_status_fails(self):
        user = UserFactory()
        booking = BookingFactory(user=user, status=Booking.Status.PAYMENT_PENDING)

        with pytest.raises(DjLodgingValidationError) as exc:
            BookingService.cancel(actor=user, booking_id=booking.id)

        assert str(exc.value) == "This booking cannot be canceled!"

    def test_cancel_booking_with_wrong_user_fails(self):
        user = UserFactory()
        wrong_user = UserFactory()
        booking = BookingFactory(user=user, status=Booking.Status.PAID)

        with pytest.raises(PermissionDenied):
            BookingService.cancel(actor=wrong_user, booking_id=booking.id)

        booking.refresh_from_db()

        assert booking.status == Booking.Status.PAID
