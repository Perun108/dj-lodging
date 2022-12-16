from uuid import UUID

from django.conf import settings

from djlodging.domain.bookings.repository import BookingRepository
from djlodging.infrastructure.providers.email import email_provider


class EmailService:
    @classmethod
    def send_confirmation_link(cls, email, security_token):
        link = f"{settings.DOMAIN}/sign-up?token={str(security_token)}&email={email}"
        return email_provider.send_confirmation_link(email=email, link=link)

    @classmethod
    def send_change_password_link(cls, email: str, token: UUID):
        link = f"{settings.DOMAIN}/change-password?token={str(token)}&email={email}"
        return email_provider.send_change_password_link(email=email, link=link)

    @classmethod
    def send_change_email_link(cls, new_email: str, token: UUID):
        link = f"{settings.DOMAIN}/change-email?token={str(token)}&email={new_email}"
        return email_provider.send_change_email_link(email=new_email, link=link)

    @classmethod
    def send_booking_confirmation_email_to_user(cls, booking_id: str):
        booking = BookingRepository.get_by_id(booking_id)
        user = booking.user
        return email_provider.send_booking_confirmation_email_to_user(
            email=user.email,
            username=user.username,
            lodging_name=booking.lodging.name,
            city=booking.lodging.city.name,
            date_from=booking.date_from.strftime("%b %d, %Y"),
            date_to=booking.date_to.strftime("%b %d, %Y"),
            reference_code=booking.reference_code,
        )

    @classmethod
    def send_booking_confirmation_email_to_owner(cls, booking_id: str):
        booking = BookingRepository.get_by_id(booking_id)
        user = booking.user
        owner = booking.lodging.owner
        return email_provider.send_booking_confirmation_email_to_owner(
            email=owner.email,
            owner_name=owner.username,
            username=user.username,
            lodging_name=booking.lodging.name,
            city=booking.lodging.city.name,
            date_from=booking.date_from.strftime("%b %d, %Y"),
            date_to=booking.date_to.strftime("%b %d, %Y"),
            reference_code=booking.reference_code,
        )

    @classmethod
    def send_booking_cancellation_email_to_user(cls, booking_id: str):
        booking = BookingRepository.get_by_id(booking_id)
        user = booking.user
        return email_provider.send_booking_cancellation_email_to_user(
            email=user.email,
            username=user.username,
            lodging_name=booking.lodging.name,
            city=booking.lodging.city.name,
            date_from=booking.date_from.strftime("%b %d, %Y"),
            date_to=booking.date_to.strftime("%b %d, %Y"),
            reference_code=booking.reference_code,
        )

    @classmethod
    def send_booking_cancellation_email_to_owner(cls, booking_id: str):
        booking = BookingRepository.get_by_id(booking_id)
        user = booking.user
        owner = booking.lodging.owner
        return email_provider.send_booking_cancellation_email_to_owner(
            email=owner.email,
            owner_name=owner.username,
            username=user.username,
            lodging_name=booking.lodging.name,
            city=booking.lodging.city.name,
            date_from=booking.date_from.strftime("%b %d, %Y"),
            date_to=booking.date_to.strftime("%b %d, %Y"),
            reference_code=booking.reference_code,
        )
