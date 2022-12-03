from uuid import UUID

from djlodging.application_services.email import EmailService
from djlodging.domain.bookings.models import Booking
from djlodging.domain.bookings.repository import BookingRepository
from djlodging.domain.users.repository import UserRepository
from djlodging.infrastructure.jobs.celery_config import app as celery_app


# ==================EMAIL TASKS=========================================
def send_confirmation_link_task(email: str, security_token: UUID):
    return EmailService.send_confirmation_link(email=email, security_token=security_token)


def send_change_password_link_task(email: str, token: UUID):
    return EmailService.send_change_password_link(email=email, token=token)


def send_change_email_link_task(new_email: str, token: UUID):
    return EmailService.send_change_email_link(new_email=new_email, token=token)


def send_booking_confirmation_email_to_user_task(booking: Booking):
    return EmailService.send_booking_confirmation_email_to_user(booking)


def send_booking_confirmation_email_to_owner_task(booking: Booking):
    return EmailService.send_booking_confirmation_email_to_owner(booking)


# ==================CELERY TASKS=========================================
@celery_app.task()
def delete_unregistered_user_after_security_token_expired(user_id):
    UserRepository.delete_by_id(user_id)


@celery_app.task()
def delete_expired_unpaid_booking(booking_id):
    BookingRepository.delete_by_id(booking_id)


# ================CELERY BEAT PERIODIC TASKS==============================
@celery_app.task
def delete_users_with_unfinished_registration():
    UserRepository.delete_users_with_unfinished_registration()


@celery_app.task
def delete_all_expired_unpaid_bookings():
    BookingRepository.delete_all_expired_unpaid_bookings()
