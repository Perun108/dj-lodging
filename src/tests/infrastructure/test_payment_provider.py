import pytest
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


@pytest.mark.django_db
class TestPaymentProvider:
    pass
