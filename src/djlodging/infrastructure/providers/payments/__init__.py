from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from .base_payment_provider import BasePaymentProvider
from .stripe_payment_provider import StripePaymentProvider

__all__ = [
    "payment_provider",
    "BasePaymentProvider",
    "StripePaymentProvider",
]


def __get_payment_provider() -> StripePaymentProvider:
    try:
        payment_provider = settings.PAYMENT_PROVIDER
    except AttributeError:
        raise ImproperlyConfigured("Requested setting PAYMENT_PROVIDER, but it's not configured.")

    try:
        payment_provider_class = import_string(payment_provider)
    except ImportError:
        raise ImproperlyConfigured(
            "Couldn't import DEFAULT_PAYMENT_PROVIDER_CLASS. Did you configure it?"
        )
    return payment_provider_class()


payment_provider = __get_payment_provider()
