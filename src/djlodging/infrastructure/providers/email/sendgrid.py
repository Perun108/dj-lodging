from django.conf import settings
from sendgrid import SendGridAPIClient

from djlodging.infrastructure.providers.email.base_email_provider import (
    BaseEmailProvider,
)


# pylint: disable=too-many-instance-attributes
class SendgridEmailProvider(BaseEmailProvider):
    """Sendgrid Email Provider class"""

    def __init__(self):
        super().__init__()
        email_provider_settings = settings.EMAIL_PROVIDER_SETTINGS
        self.sendgrid_api = SendGridAPIClient(api_key=email_provider_settings["API_KEY"])
        self.confirmation_link_template_id = email_provider_settings[
            "CONFIRMATION_LINK_TEMPLATE_ID"
        ]

        self.change_password_link_template_id = email_provider_settings[
            "CHANGE_PASSWORD_LINK_TEMPLATE_ID"
        ]
        self.change_password_link_template_id = email_provider_settings[
            "CHANGE_PASSWORD_LINK_TEMPLATE_ID"
        ]
        self.change_email_link_template_id = email_provider_settings[
            "CHANGE_EMAIL_LINK_TEMPLATE_ID"
        ]
        self.booking_confirmation_email_for_user_template_id = email_provider_settings[
            "BOOKING_CONFIRMATION_EMAIL_FOR_USER_TEMPLATE_ID"
        ]
        self.booking_confirmation_email_for_owner_template_id = email_provider_settings[
            "BOOKING_CONFIRMATION_EMAIL_FOR_OWNER_TEMPLATE_ID"
        ]
        self.booking_cancellation_email_to_user_template_id = email_provider_settings[
            "BOOKING_CANCELLATION_EMAIL_FOR_USER_TEMPLATE_ID"
        ]
        self.booking_cancellation_email_to_owner_template_id = email_provider_settings[
            "BOOKING_CANCELLATION_EMAIL_FOR_OWNER_TEMPLATE_ID"
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

    def send_booking_confirmation_email_to_user(
        self,
        *,
        email: str,
        username: str,
        lodging_name: str,
        city: str,
        date_from: str,
        date_to: str,
        reference_code: str,
    ) -> dict:
        data = {
            "personalizations": [
                {
                    "to": [{"email": email}],
                    "dynamic_template_data": {
                        "user_email": email,
                        "username": username,
                        "lodging_name": lodging_name,
                        "city": city,
                        "date_from": date_from,
                        "date_to": date_to,
                        "reference_code": reference_code,
                    },
                }
            ],
            "from": {"email": self.from_email},
            "template_id": self.booking_confirmation_email_for_user_template_id,
        }
        return self.sendgrid_api.client.mail.send.post(request_body=data)

    def send_booking_confirmation_email_to_owner(
        self,
        *,
        email: str,
        owner_name: str,
        username: str,
        lodging_name: str,
        city: str,
        date_from: str,
        date_to: str,
        reference_code: str,
    ) -> dict:
        data = {
            "personalizations": [
                {
                    "to": [{"email": email}],
                    "dynamic_template_data": {
                        "owner_email": email,
                        "owner_name": owner_name,
                        "username": username,
                        "lodging_name": lodging_name,
                        "city": city,
                        "date_from": date_from,
                        "date_to": date_to,
                        "reference_code": reference_code,
                    },
                }
            ],
            "from": {"email": self.from_email},
            "template_id": self.booking_confirmation_email_for_owner_template_id,
        }
        return self.sendgrid_api.client.mail.send.post(request_body=data)

    def send_booking_cancellation_email_to_user(
        self,
        *,
        email: str,
        username: str,
        lodging_name: str,
        city: str,
        date_from: str,
        date_to: str,
    ) -> dict:
        data = {
            "personalizations": [
                {
                    "to": [{"email": email}],
                    "dynamic_template_data": {
                        "user_email": email,
                        "username": username,
                        "lodging_name": lodging_name,
                        "city": city,
                        "date_from": date_from,
                        "date_to": date_to,
                    },
                }
            ],
            "from": {"email": self.from_email},
            "template_id": self.booking_cancellation_email_to_user_template_id,
        }
        return self.sendgrid_api.client.mail.send.post(request_body=data)

    def send_booking_cancellation_email_to_owner(
        self,
        *,
        email: str,
        owner_name: str,
        username: str,
        lodging_name: str,
        city: str,
        date_from: str,
        date_to: str,
        reference_code: str,
    ) -> dict:
        data = {
            "personalizations": [
                {
                    "to": [{"email": email}],
                    "dynamic_template_data": {
                        "owner_email": email,
                        "owner_name": owner_name,
                        "username": username,
                        "lodging_name": lodging_name,
                        "city": city,
                        "date_from": date_from,
                        "date_to": date_to,
                        "reference_code": reference_code,
                    },
                }
            ],
            "from": {"email": self.from_email},
            "template_id": self.booking_cancellation_email_to_owner_template_id,
        }
        return self.sendgrid_api.client.mail.send.post(request_body=data)
