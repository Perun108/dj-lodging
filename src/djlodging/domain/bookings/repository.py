from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from djlodging.domain.bookings.models import Booking
from djlodging.domain.users.models import User


class BookingRepository:
    @classmethod
    def save(cls, booking: Booking) -> None:
        booking.save()

    @classmethod
    def get_list(cls, user: User) -> QuerySet[Booking]:
        return Booking.objects.filter(user=user)

    @classmethod
    def get_by_id(cls, booking_id):
        try:
            return Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            raise ValidationError("Wrong booking_id")