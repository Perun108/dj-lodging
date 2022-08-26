from abc import ABC, abstractmethod


class BasePaymentProvider(ABC):
    """Abstract Base PaymentProvider class"""

    @abstractmethod
    def get_payment_provider_customer(self):
        pass

    @abstractmethod
    def create_payment_user(self):
        pass

    @abstractmethod
    def create_payment_intent(self):
        pass

    @abstractmethod
    def get_payment_intent(self):
        pass
