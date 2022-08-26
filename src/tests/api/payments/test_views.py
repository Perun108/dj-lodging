import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from djlodging.infrastructure.providers.payments import payment_provider
from tests.domain.bookings.factories import BookingFactory


@pytest.mark.django_db
class TestPaymentViewSet:
    def test_pay_succeeds(self, user_api_client_pytest_fixture, user):
        booking = BookingFactory(user=user)
        metadata = {"booking_id": str(booking.id)}
        payload = {"metadata": metadata}
        url = reverse("payment-pay")
        response = user_api_client_pytest_fixture.post(url, payload, format="json")

        assert response.status_code == HTTP_201_CREATED
        assert "client_secret" in response.data
        assert response.data["client_secret"].startswith("pi_") is True
        assert "_secret_" in response.data["client_secret"]

        ind = response.data["client_secret"].index("_secret_")
        payment_intent_id = response.data["client_secret"][:ind]
        payment_intent = payment_provider.get_payment_intent(payment_intent_id)

        assert int(payment_intent.amount / 100) == int(booking.lodging.price)
        assert payment_intent.client_secret == response.data["client_secret"]
        assert payment_intent["metadata"] == metadata
        assert payment_intent.payment_method is None
        assert payment_intent.status == "requires_payment_method"

    def test_pay_by_another_user_fails(self, user_api_client_pytest_fixture, user):
        booking = BookingFactory()

        payload = {"metadata": {"booking_id": booking.id}}
        url = reverse("payment-pay")
        response = user_api_client_pytest_fixture.post(url, payload, format="json")

        assert response.status_code == HTTP_403_FORBIDDEN
        assert str(response.data["detail"]) == "You do not have permission to perform this action."
