from django.core.exceptions import ValidationError


class RegistrationTimePassed(ValidationError):
    def __init__(self, code=None, params=None) -> None:
        message = "Your sign up time has already passed. Please start registration again."
        super().__init__(message=message, code=code, params=params)


class WrongBookingReferenceCode(ValidationError):
    def __init__(self, code=None, params=None) -> None:
        message = (
            "We couldn't find a booking with this reference code among your bookings. "
            + "Make sure that you entered a correct reference code."
        )
        super().__init__(message=message, code=code, params=params)


class WrongLodgingError(ValidationError):
    def __init__(self, code=None, params=None) -> None:
        message = "This code refers to another lodging that you stayed in. "
        "Please enter the correct code or select another lodging for review."
        super().__init__(message=message, code=code, params=params)


class WrongOwnerError(ValidationError):
    def __init__(self, code=None, params=None) -> None:
        message = "You cannot modify this lodging since you are not its owner."
        super().__init__(message=message, code=code, params=params)
