from uuid import UUID

from django.conf import settings

from djlodging.domain.users.repository import UserRepository
from djlodging.infrastructure.providers.email import email_provider


class EmailService:
    @classmethod
    def send_confirmation_link(cls, user_id):
        user = UserRepository.get_by_id(user_id)
        link = f"{settings.DOMAIN}/sign-up/{str(user.security_token)}"
        return email_provider.send_confirmation_link(email=user.email, link=link)

    @classmethod
    def send_change_password_link(cls, email: str, token: UUID):
        link = f"{settings.DOMAIN}/change-password/{str(token)}"
        return email_provider.send_change_password_link(email=email, link=link)
