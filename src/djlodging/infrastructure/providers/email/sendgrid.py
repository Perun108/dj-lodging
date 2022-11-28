from django.conf import settings
from sendgrid import SendGridAPIClient

from djlodging.infrastructure.providers.email.base_email_provider import (
    BaseEmailProvider,
)


class SendgridEmailProvider(BaseEmailProvider):
    """Sendgrid Email Provider class"""

    def __init__(self):
        super().__init__()

        self.sendgrid_api = SendGridAPIClient(api_key=settings.EMAIL_PROVIDER["API_KEY"])
        self.confirmation_link_template_id = settings.EMAIL_PROVIDER[
            "CONFIRMATION_LINK_TEMPLATE_ID"
        ]

        self.change_password_link_template_id = settings.EMAIL_PROVIDER[
            "CHANGE_PASSWORD_LINK_TEMPLATE_ID"
        ]
        self.change_password_link_template_id = settings.EMAIL_PROVIDER[
            "CHANGE_PASSWORD_LINK_TEMPLATE_ID"
        ]
        self.change_email_link_template_id = settings.EMAIL_PROVIDER[
            "CHANGE_EMAIL_LINK_TEMPLATE_ID"
        ]

    def send_confirmation_link(
        self,
        *,
        email: str,
        link: str,
    ) -> dict:
        data = {
            "personalizations": [
                {
                    "to": [{"email": email}],
                    "dynamic_template_data": {
                        "email": email,
                        "link": link,
                    },
                }
            ],
            "from": {"email": self.from_email},
            "template_id": self.confirmation_link_template_id,
        }
        return self.sendgrid_api.client.mail.send.post(request_body=data)

    def send_change_password_link(
        self,
        *,
        email: str,
        link: str,
    ) -> dict:
        data = {
            "personalizations": [
                {
                    "to": [{"email": email}],
                    "dynamic_template_data": {
                        "email": email,
                        "link": link,
                    },
                }
            ],
            "from": {"email": self.from_email},
            "template_id": self.change_password_link_template_id,
        }
        return self.sendgrid_api.client.mail.send.post(request_body=data)

    def send_forgot_password_email(self, *, email: str, username: str, link: str) -> dict:
        data = {
            "personalizations": [
                {
                    "to": [{"email": email}],
                    "dynamic_template_data": {"name": username, "user_email": email, "link": link},
                }
            ],
            "from": {"email": self.from_email},
            "template_id": self.forgot_password_template_id,
        }
        return self.sendgrid_api.client.mail.send.post(request_body=data)

    def send_change_email_link(self, *, email: str, link: str) -> dict:
        data = {
            "personalizations": [
                {
                    "to": [{"email": email}],
                    "dynamic_template_data": {"user_email": email, "link": link},
                }
            ],
            "from": {"email": self.from_email},
            "template_id": self.change_email_link_template_id,
        }
        return self.sendgrid_api.client.mail.send.post(request_body=data)
