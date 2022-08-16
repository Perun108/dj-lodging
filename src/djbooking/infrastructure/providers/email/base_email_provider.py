from abc import ABC, abstractmethod

from django.conf import settings


class BaseEmailProvider(ABC):
    """Abstract Base EmailProvider class"""

    def __init__(self):
        super().__init__()
        self.from_email = settings.EMAIL_PROVIDER["DEFAULT_FROM_EMAIL"]

    @abstractmethod
    def send_confirmation_code(self, *, email: str, code: str):
        pass

    @abstractmethod
    def send_forgot_password_email(self, *, email: str, username: str, link: str):
        pass
