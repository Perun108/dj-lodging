from django.core.exceptions import PermissionDenied

from djlodging.domain.bookings.repository import BookingRepository
from djlodging.infrastructure.providers.payments import payment_provider


class PaymentService:
    @classmethod
    def pay(cls, user, metadata, currency="usd", capture_method="automatic"):
        booking = BookingRepository.get_by_id(metadata["booking_id"])

        if user != booking.user:
            raise PermissionDenied

        payment_intent = payment_provider.create_payment_intent(
            user=user,
            amount=booking.lodging.price,
            currency=currency,
            metadata=metadata,
            capture_method=capture_method,
        )
        return payment_intent.client_secret
