from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID


class BasePaymentProvider(ABC):
    """Abstract Base PaymentProvider class"""

    @abstractmethod
    def create_payment_user(self, email: str):
        pass

    @abstractmethod
    def create_payment_intent(
        self,
        customer_id: UUID,
        amount: Decimal,
        currency: str,
        metadata: dict,
        capture_method: str,
        receipt_email: str,
    ):
        pass

    @abstractmethod
    def get_payment_intent(self, payment_intent_id: str):
        pass

    @abstractmethod
    def create_refund(
        self,
        amount: Decimal,
        payment_intent_id: str,
        metadata: dict,
    ):
        pass
