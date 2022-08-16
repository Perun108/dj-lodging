from django.conf import settings
from sendgrid import SendGridAPIClient

from djbooking.infrastructure.providers.email.base_email_provider import (
    BaseEmailProvider,
)


class SendgridEmailProvider(BaseEmailProvider):
    """Sendgrid Email Provider class"""

    def __init__(self):
        super().__init__()

        self.sendgrid_api = SendGridAPIClient(api_key=settings.EMAIL_PROVIDER["API_KEY"])
        self.confirmation_code_template_id = settings.EMAIL_PROVIDER[
            "CONFIRMATION_CODE_TEMPLATE_ID"
        ]

    def send_confirmation_code(
        self,
        *,
        email: str,
        code: str,
    ) -> dict:
        data = {
            "personalizations": [
                {
                    "to": [{"email": email}],
                    "dynamic_template_data": {
                        "email": email,
                        "code": code,
                    },
                }
            ],
            "from": {"email": self.from_email},
            "template_id": self.confirmation_code_template_id,
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
