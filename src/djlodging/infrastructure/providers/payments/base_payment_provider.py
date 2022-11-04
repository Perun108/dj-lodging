from abc import ABC, abstractmethod
from decimal import Decimal


class BasePaymentProvider(ABC):
    """Abstract Base PaymentProvider class"""

    @abstractmethod
    def create_payment_user(self, email):
        pass

    @abstractmethod
    def create_payment_intent(
        self, customer_id, amount, currency, metadata, capture_method, receipt_email
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
