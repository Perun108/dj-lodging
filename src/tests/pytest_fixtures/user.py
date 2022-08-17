import pytest
from faker import Faker

from djlodging.domain.users.models import User

fake = Faker()


@pytest.fixture
def password():
    return fake.password()


@pytest.fixture
def user(password):
    email = "example@example.com"
    user = User.objects.create_user(email=email, password=password, username="TestUser")
    return user
