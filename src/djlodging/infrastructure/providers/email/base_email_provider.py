from abc import ABC, abstractmethod

from django.conf import settings


class BaseEmailProvider(ABC):
    """Abstract Base EmailProvider class"""

    def __init__(self):
        super().__init__()
        self.from_email = settings.EMAIL_PROVIDER["DEFAULT_FROM_EMAIL"]

    @abstractmethod
    def send_confirmation_link(self, *, email: str, link: str):
        pass

    @abstractmethod
    def send_change_password_link(self, *, email: str, link: str):
        pass

    @abstractmethod
    def send_forgot_password_email(self, *, email: str, username: str, link: str):
        pass
