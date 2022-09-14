from uuid import UUID

from django.conf import settings

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
