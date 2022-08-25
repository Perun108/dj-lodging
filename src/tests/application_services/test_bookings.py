import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from faker import Faker

from djlodging.application_services.bookings import BookingService
from djlodging.domain.bookings.models import Booking
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

        with pytest.raises(ValidationError) as exc:
            BookingService.create(
                lodging_id=lodging.id, user=user, date_from=date_from, date_to=date_to
            )
        assert str(exc.value) == "['The dates are invalid']"

        booking = Booking.objects.first()
        assert booking is None

    def test_create_booking_with_invalid_date_to_fails(self):
        lodging = LodgingFactory()
        user = UserFactory()
        date_from = timezone.now().date() + timezone.timedelta(days=1)
        date_to = date_from - timezone.timedelta(days=2)

        with pytest.raises(ValidationError) as exc:
            BookingService.create(
                lodging_id=lodging.id, user=user, date_from=date_from, date_to=date_to
            )
        assert str(exc.value) == "['The dates are invalid']"

        booking = Booking.objects.first()
        assert booking is None

    def test_create_booking_with_equal_dates_fails(self):
        lodging = LodgingFactory()
        user = UserFactory()
        date_from = timezone.now().date() - timezone.timedelta(days=1)
        date_to = date_from

        with pytest.raises(ValidationError) as exc:
            BookingService.create(
                lodging_id=lodging.id, user=user, date_from=date_from, date_to=date_to
            )
        assert str(exc.value) == "['Please provide date_to']"

        booking = Booking.objects.first()
        assert booking is None

    def test_create_booking_with_date_from_greater_than_date_to_fails(self):
        lodging = LodgingFactory()
        user = UserFactory()
        date_from = timezone.now().date() + timezone.timedelta(days=2)
        date_to = timezone.now().date()

        with pytest.raises(ValidationError) as exc:
            BookingService.create(
                lodging_id=lodging.id, user=user, date_from=date_from, date_to=date_to
            )
        assert str(exc.value) == "['The dates are invalid']"

        booking = Booking.objects.first()
        assert booking is None
