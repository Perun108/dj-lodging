from djlodging.domain.core.base_exceptions import BaseDjLodgingError


class RegistrationTimePassed(BaseDjLodgingError):
    def __init__(self, extra=None):
        message = "Your sign up time has already passed. Please start registration again."
        super().__init__(message, extra)


class LodgingAlreadyBookedError(BaseDjLodgingError):
    def __init__(self, extra=None):
        message = "This lodging is already booked for these dates"
        super().__init__(message, extra)


class PaymentExpirationTimePassed(BaseDjLodgingError):
    def __init__(self, extra=None):
        message = "The time for payment has already passed. Please start the booking again."
        super().__init__(message, extra)


class WrongBookingReferenceCode(BaseDjLodgingError):
    def __init__(self, extra=None):
        message = (
            "We couldn't find a booking with this reference code among your bookings. "
            + "Make sure that you entered a correct reference code."
        )
        super().__init__(message, extra)


class WrongLodgingError(BaseDjLodgingError):
    def __init__(self, extra=None):
        message = (
            "This code refers to another lodging that you stayed in. "
            + "Please enter the correct code or select another lodging for review."
        )
        super().__init__(message, extra)


class WrongOwnerError(BaseDjLodgingError):
    def __init__(self, extra=None):
        message = "You cannot modify this lodging since you are not its owner."
        super().__init__(message, extra)
