from djlodging.infrastructure.providers.provider_injector import get_provider

from .base_payment_provider import BasePaymentProvider
from .stripe_payment_provider import StripePaymentProvider

__all__ = [
    "payment_provider",
    "BasePaymentProvider",
    "StripePaymentProvider",
]

payment_provider = get_provider("PAYMENT_PROVIDER")
