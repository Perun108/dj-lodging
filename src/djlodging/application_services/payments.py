from decimal import Decimal

from djlodging.domain.core.base_exceptions import DjLodgingValidationError
from djlodging.domain.users.models import User
from djlodging.infrastructure.providers.payments import payment_provider


class PaymentService:
    @classmethod
    def create_payment(
        cls,
        user: User,
        price: Decimal,
        metadata: dict,
        currency: str = "usd",
        capture_method: str = "automatic",
    ):
        if not hasattr(user, "payment_user"):
            raise DjLodgingValidationError(
                "Payments were not properly assigned to this user. "
                + "Please go through all steps during registration."
            )
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
    def create_refund(cls, payment_intent_id: str, price: Decimal, metadata: dict):
        refund = payment_provider.create_refund(
            payment_intent_id=payment_intent_id,
            amount=price,
            metadata=metadata,
        )
        return refund
