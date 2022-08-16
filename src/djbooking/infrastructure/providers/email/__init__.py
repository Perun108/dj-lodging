from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from .base_email_provider import BaseEmailProvider
from .sendgrid import SendgridEmailProvider

__all__ = [
    "email_provider",
    "BaseEmailProvider",
    "SendgridEmailProvider",
]


def __get_email_provider() -> SendgridEmailProvider:
    try:
        email_provider = settings.EMAIL_PROVIDER["DEFAULT_EMAIL_PROVIDER_CLASS"]
    except AttributeError:
        raise ImproperlyConfigured("Requested setting EMAIL_PROVIDER, but it's not configured.")

    try:
        email_provider_class = import_string(email_provider)
    except ImportError:
        raise ImproperlyConfigured(
            "Couldn't import DEFAULT_EMAIL_PROVIDER_CLASS. Did you configure it?"
        )
    return email_provider_class()


email_provider = __get_email_provider()
