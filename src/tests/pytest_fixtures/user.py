import pytest
from faker import Faker

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
