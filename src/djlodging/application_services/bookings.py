from datetime import date
from uuid import UUID

from django.core.exceptions import ValidationError
from django.utils import timezone

from djlodging.domain.bookings.models import Booking
from djlodging.domain.bookings.repository import BookingRepository
from djlodging.domain.lodgings.repositories import LodgingRepository
from djlodging.domain.users.models import User


class BookingService:
    @classmethod
    def _validate_dates(cls, date_from, date_to):
        now = timezone.now().date()
        if date_from == date_to:
            raise ValidationError("Please provide date_to")
        if any([date_from < now, date_to < now, date_from > date_to]):
            raise ValidationError("The dates are invalid")

    @classmethod
    def _validate_lodging_availability(cls, lodging_id: UUID, date_from: date, date_to: date):
        lodging = LodgingRepository.get_by_id(lodging_id)
        for booking in lodging.booking.all():
            if (
                booking.date_from <= date_from < booking.date_to
                or booking.date_from < date_to <= booking.date_to
            ):
                raise ValidationError("This lodging is already booked for these dates")
        return lodging

    @classmethod
    def create(cls, lodging_id: UUID, user: User, date_from: date, date_to: date) -> Booking:
        cls._validate_dates(date_from, date_to)
        lodging = cls._validate_lodging_availability(lodging_id, date_from, date_to)
        booking = Booking(lodging=lodging, user=user, date_from=date_from, date_to=date_to)
        BookingRepository.save(booking)
        return booking

    @classmethod
    def confirm_booking(cls, metadata):
        booking = BookingRepository.get_by_id(metadata["booking_id"])
        booking.status = Booking.Status.PAID
        BookingRepository.save(booking)
