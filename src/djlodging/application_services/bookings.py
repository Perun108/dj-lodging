from datetime import date
from uuid import UUID

from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone

from djlodging.application_services.payments import PaymentService
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
    def retrieve(cls, actor: User, booking_id: UUID) -> Booking:
        if not actor.is_staff:
            raise PermissionDenied
        return BookingRepository.get_by_id(booking_id)

    @classmethod
    def pay(cls, actor, booking_id: UUID, currency="usd", capture_method="automatic"):
        booking = BookingRepository.get_by_id(booking_id)

        if actor != booking.user:
            raise PermissionDenied

        metadata = {"booking_id": booking.id}

        payment_intent = PaymentService.create_payment(
            actor, booking.lodging.price, metadata, currency, capture_method
        )
        cls._set_booking_payment_intent_id(booking, payment_intent.id)
        return payment_intent.client_secret

    @classmethod
    def _set_booking_payment_intent_id(cls, booking, payment_intent_id: str):
        booking.payment_intent_id = payment_intent_id
        BookingRepository.save(booking)

    @classmethod
    def confirm(cls, metadata):
        booking = BookingRepository.get_by_id(metadata["booking_id"])
        BookingRepository.change_status(booking, new_status=Booking.Status.PAID)

    @classmethod
    def cancel(cls, actor: User, booking_id: UUID) -> Booking:
        booking = BookingRepository.get_by_id(booking_id)
        if actor != booking.user:
            raise PermissionDenied
        if booking.status != Booking.Status.PAID:
            raise ValidationError("This booking cannot be canceled!")

        PaymentService.create_refund(
            payment_intent_id=booking.payment_intent_id,
            price=booking.lodging.price,
            metadata={"booking_id": booking.id},
        )
        booking = BookingRepository.change_status(booking, new_status=Booking.Status.CANCELED)
        return booking

    @classmethod
    def get_filtered_paginated_list(cls, actor: User, query_params) -> dict:
        if not actor.is_staff:
            raise PermissionDenied
        return BookingRepository.get_filtered_list(query_params)
