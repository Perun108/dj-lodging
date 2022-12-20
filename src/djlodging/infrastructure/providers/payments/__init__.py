from typing import Union

from djlodging.infrastructure.providers.provider_injector import get_provider

from .base_payment_provider import BasePaymentProvider
from .stripe_payment_provider import StripePaymentProvider

payment_provider_type = Union[BasePaymentProvider, StripePaymentProvider]

payment_provider: payment_provider_type = get_provider("PAYMENT_PROVIDER")

__all__ = [
    "payment_provider",
    "BasePaymentProvider",
    "StripePaymentProvider",
]
