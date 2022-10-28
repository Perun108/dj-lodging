from datetime import date, timedelta

import pytest
import stripe
from django.conf import settings
from faker import Faker

from djlodging.application_services.users import PaymentProviderUserService
from djlodging.domain.users.models import User

fake = Faker()


@pytest.fixture
def password():
    return fake.password()


@pytest.fixture
def user(password):
    email = "test_user@example.com"
    user = User.objects.create_user(email=email, password=password, username="TestUser")
    return user


@pytest.fixture
def partner(password):
    email = "test_partner@example.com"
    user = User.objects.create_user(
        email=email, password=password, username="TestPartner", is_partner=True
    )
    return user


@pytest.fixture
def admin(password):
    email = "test_admin@example.com"
    user = User.objects.create_user(
        email=email, password=password, username="TestPartner", is_staff=True
    )
    return user


# Fixtures for integration tests
stripe.api_key = settings.STRIPE_API_KEY


@pytest.fixture
def payment_method():
    payment_method = stripe.PaymentMethod.create(
        type="card",
        card={
            "number": "4242424242424242",
            "exp_month": 12,
            "exp_year": (date.today() + timedelta(weeks=52)).year,
            "cvc": "314",
        },
    )
    return payment_method


@pytest.fixture
def user_with_payment(password, payment_method):
    email = "test_user_payments@example.com"
    user = User.objects.create_user(email=email, password=password, username="TestUserPayment")
    PaymentProviderUserService.create(user)
    stripe.PaymentMethod.attach(
        payment_method.id,
        customer=user.payment_user.customer_id,
    )
    return user
