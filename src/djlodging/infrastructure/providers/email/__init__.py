from typing import Union

from djlodging.infrastructure.providers.provider_injector import get_provider

from .base_email_provider import BaseEmailProvider
from .sendgrid import SendgridEmailProvider

email_provider_type = Union[BaseEmailProvider, SendgridEmailProvider]

email_provider: email_provider_type = get_provider("EMAIL_PROVIDER")

__all__ = [
    "email_provider",
    "BaseEmailProvider",
    "SendgridEmailProvider",
]
