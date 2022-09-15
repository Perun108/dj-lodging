from decimal import Decimal

import stripe
from django.conf import settings
from django.core.exceptions import ValidationError
from djstripe import webhooks
from djstripe.models import Customer
from stripe.error import InvalidRequestError

from djlodging.infrastructure.providers.payments.base_payment_provider import (
    BasePaymentProvider,
)

stripe.api_key = settings.STRIPE_API_KEY


class StripePaymentProvider(BasePaymentProvider):
    def get_payment_provider_customer(self):
        return Customer

    def create_payment_user(self, *, email: str) -> stripe.Customer:
        """Create a stripe customer."""
        return stripe.Customer.create(email=email)

    def create_payment_intent(self, user, amount, currency, metadata, capture_method):
        amount_in_cents = int(amount * 100)
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency=currency,
            customer=user.payment_user.customer_id,
            capture_method=capture_method,
            metadata=metadata,
            receipt_email=user.email,
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
        except InvalidRequestError as ex:
            raise ValidationError(message=ex.user_message)


@webhooks.handler("payment_intent.succeeded")
def confirm_payment(event, **kwargs):
    """Change booking status to 'PAID'"""
    from djlodging.application_services.bookings import BookingService

    payment_intent = event.data["object"]
    BookingService.confirm(payment_intent["metadata"])
