from decimal import Decimal

import stripe
from django.conf import settings
from djstripe import webhooks
from stripe.error import InvalidRequestError

from djlodging.infrastructure.providers.payments.base_payment_provider import (
    BasePaymentProvider,
)
from djlodging.infrastructure.providers.payments.exceptions import (
    PaymentProviderException,
)

stripe.api_key = settings.STRIPE_API_KEY


class StripePaymentProvider(BasePaymentProvider):
    def create_payment_user(self, email: str) -> stripe.Customer:
        """Create a stripe customer."""
        return stripe.Customer.create(email=email)

    def create_payment_intent(
        self, customer_id, amount, currency, metadata, capture_method, receipt_email
    ):
        amount_in_cents = int(amount * 100)
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency=currency,
            customer=customer_id,
            capture_method=capture_method,
            metadata=metadata,
            receipt_email=receipt_email,
        )
        return payment_intent

    def get_payment_intent(self, payment_intent_id: str):
        return stripe.PaymentIntent.retrieve(id=payment_intent_id)

    def create_refund(
        self,
        amount: Decimal,
        payment_intent_id: str,
        metadata: dict,
    ):
        amount_in_cents = int(amount * 100)
        try:
            return stripe.Refund.create(
                payment_intent=payment_intent_id, amount=amount_in_cents, metadata=metadata
            )
        except InvalidRequestError as exc:
            raise PaymentProviderException(message=exc.user_message) from exc


@webhooks.handler("payment_intent.succeeded")
def confirm_payment(event, **kwargs):
    """Change booking status to 'PAID'"""
    # pylint: disable=import-outside-toplevel
    from djlodging.application_services.bookings import BookingService

    payment_intent = event.data["object"]
    BookingService.confirm(payment_intent["metadata"])
