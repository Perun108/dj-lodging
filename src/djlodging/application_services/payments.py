from djlodging.domain.users.models import User
from djlodging.infrastructure.providers.payments import payment_provider


class PaymentService:
    @classmethod
    def create_payment(
        cls, user: User, price, metadata, currency="usd", capture_method="automatic"
    ):
        payment_intent = payment_provider.create_payment_intent(
            customer_id=user.payment_user.customer_id,
            amount=price,
            currency=currency,
            metadata=metadata,
            capture_method=capture_method,
            receipt_email=user.email,
        )
        return payment_intent

    @classmethod
    def create_refund(cls, payment_intent_id, price, metadata):
        payment_intent = payment_provider.create_refund(
            payment_intent_id=payment_intent_id,
            amount=price,
            metadata=metadata,
        )
        return payment_intent
