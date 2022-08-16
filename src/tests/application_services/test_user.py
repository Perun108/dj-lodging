import pytest
from django.contrib.auth.hashers import check_password
from faker import Faker

from djbooking.application_services.users import UserService

fake = Faker()


@pytest.mark.django_db
class TestUserService:
    def test_create(self):
        email = fake.email()
        password = fake.password()
        # print(str(password))
        user = UserService.create(email=email, password=password)

        assert user is not None
        assert user.email == email
        assert user.password != password
        assert check_password(str(password), user.password) is True
