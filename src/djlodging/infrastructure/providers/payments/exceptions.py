from djlodging.domain.core.base_exceptions import BaseDjLodgingError


class PaymentProviderException(BaseDjLodgingError):
    def __init__(self, message, extra=None):
        super().__init__(message, extra)
