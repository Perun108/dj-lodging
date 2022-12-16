from abc import ABC, abstractmethod

from django.conf import settings


class BaseEmailProvider(ABC):
    """Abstract Base EmailProvider class"""

    def __init__(self):
        super().__init__()
        self.from_email = settings.DEFAULT_FROM_EMAIL

    @abstractmethod
    def send_confirmation_link(self, *, email: str, link: str):
        pass

    @abstractmethod
    def send_change_password_link(self, *, email: str, link: str):
        pass

    @abstractmethod
    def send_forgot_password_email(self, *, email: str, username: str, link: str):
        pass

    @abstractmethod
    def send_change_email_link(self, *, email: str, link: str):
        pass

    @abstractmethod
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
    ):
        pass

    @abstractmethod
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
    ):
        pass

    @abstractmethod
    def send_booking_cancellation_email_to_user(
        self,
        *,
        email: str,
        username: str,
        lodging_name: str,
        city: str,
        date_from: str,
        date_to: str,
        reference_code: str,
    ):
        pass

    @abstractmethod
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
    ):
        pass
