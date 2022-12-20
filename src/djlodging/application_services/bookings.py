from datetime import date
from uuid import UUID

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now, timedelta

from djlodging.application_services.exceptions import (
    LodgingAlreadyBookedError,
    PaymentExpirationTimePassed,
)
from djlodging.application_services.payments import PaymentService
from djlodging.domain.bookings.models import Booking
from djlodging.domain.bookings.repository import BookingRepository
from djlodging.domain.core.base_exceptions import DjLodgingValidationError
from djlodging.domain.lodgings.repositories import LodgingRepository
from djlodging.domain.users.models import User
from djlodging.infrastructure.jobs.celery_tasks import (
    delete_expired_unpaid_booking,
    send_booking_cancellation_email_to_owner_task,
    send_booking_cancellation_email_to_user_task,
    send_booking_confirmation_email_to_owner_task,
    send_booking_confirmation_email_to_user_task,
)


class BookingService:
    @classmethod
    def _validate_dates(cls, date_from, date_to):
        current_date = now().date()
        if date_from >= date_to:
            raise DjLodgingValidationError("Date_to must be greater than date_from")
        if date_from < current_date or date_to < current_date:
            raise DjLodgingValidationError("The dates are invalid")

    @classmethod
    def _check_lodging_availability(cls, lodging_id: UUID, date_from: date, date_to: date):
        lodging = LodgingRepository.get_by_id(lodging_id)
        for booking in lodging.booking.all():
            if booking.status != Booking.Status.CANCELED and (
                booking.date_from <= date_from < booking.date_to
                or booking.date_from < date_to <= booking.date_to
            ):
                raise LodgingAlreadyBookedError
        return lodging

    @classmethod
    def create(cls, lodging_id: UUID, user: User, date_from: date, date_to: date) -> Booking:
        cls._validate_dates(date_from, date_to)
        lodging = cls._check_lodging_availability(lodging_id, date_from, date_to)
        booking = Booking(
            lodging=lodging,
            user=user,
            date_from=date_from,
            date_to=date_to,
            payment_expiration_time=now()
            + timedelta(minutes=settings.BOOKING_PAYMENT_EXPIRATION_TIME_IN_MINUTES),
        )
        BookingRepository.save(booking)
        return booking

    @classmethod
    def retrieve(cls, actor: User, booking_id: UUID) -> Booking:
        if not actor.is_staff:
            raise PermissionDenied
        return BookingRepository.get_by_id(booking_id)

    @classmethod
    def pay(cls, actor, booking_id: UUID, currency="usd", capture_method="automatic") -> str:
        booking = cls._validate_booking_for_payment(actor, booking_id)
        metadata = {"booking_id": booking.id}
        payment_intent = PaymentService.create_payment(
            actor, booking.lodging.price, metadata, currency, capture_method
        )
        cls._set_booking_payment_intent_id(booking, payment_intent.id)
        return payment_intent.client_secret

    @classmethod
    def _validate_booking_for_payment(cls, actor: User, booking_id: UUID) -> Booking:
        booking = BookingRepository.get_by_id(booking_id)
        if actor != booking.user:
            raise PermissionDenied

        if booking.payment_expiration_time < now():
            delete_expired_unpaid_booking.apply_async(args=[booking_id])
            raise PaymentExpirationTimePassed

        return booking

    @classmethod
    def _set_booking_payment_intent_id(cls, booking, payment_intent_id: str):
        booking.payment_intent_id = payment_intent_id
        BookingRepository.save(booking)

    @classmethod
    def confirm(cls, metadata):
        booking = BookingRepository.get_by_id(metadata["booking_id"])
        BookingRepository.change_status(booking, new_status=Booking.Status.PAID)
        send_booking_confirmation_email_to_user_task(str(booking.id))
        send_booking_confirmation_email_to_owner_task(str(booking.id))

    @classmethod
    def cancel(cls, actor: User, booking_id: UUID) -> Booking:
        booking = cls._validate_booking_for_cancellation(actor, booking_id)

        PaymentService.create_refund(
            payment_intent_id=booking.payment_intent_id,
            price=booking.lodging.price,
            metadata={"booking_id": booking.id},
        )
        booking = BookingRepository.change_status(booking, new_status=Booking.Status.CANCELED)
        send_booking_cancellation_email_to_owner_task(str(booking.id))
        send_booking_cancellation_email_to_user_task(str(booking.id))
        return booking

    @classmethod
    def _validate_booking_for_cancellation(cls, actor: User, booking_id: UUID) -> Booking:
        booking = BookingRepository.get_by_id(booking_id)
        if actor != booking.user:
            raise PermissionDenied
        if booking.status != Booking.Status.PAID:
            raise DjLodgingValidationError("This booking cannot be canceled!")
        return booking

    @classmethod
    def get_filtered_paginated_list(cls, actor: User, query_params) -> dict:
        if not actor.is_staff:
            raise PermissionDenied
        return BookingRepository.get_filtered_list(query_params)
