import stripe
from django.conf import settings
from djstripe import webhooks
from djstripe.models import Customer

from djlodging.application_services.bookings import BookingService
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


@webhooks.handler("payment_intent")
def confirm_payment(event, **kwargs):
    """Change booking status to 'PAID'"""

    if event.type == "payment_intent.succeeded":
        payment_intent = event.data["object"]
        BookingService.confirm_booking(payment_intent["metadata"])
