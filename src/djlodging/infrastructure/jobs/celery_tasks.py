from djlodging.domain.users.repository import UserRepository
from djlodging.infrastructure.jobs.celery_config import app as celery_app


@celery_app.task
def delete_users_with_unfinished_registration():
    UserRepository.delete_users_with_unfinished_registration()
