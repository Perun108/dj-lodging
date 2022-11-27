from djlodging.domain.bookings.repository import BookingRepository
from djlodging.domain.users.repository import UserRepository
from djlodging.infrastructure.jobs.celery_config import app as celery_app


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
