import pytest
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from faker import Faker

from djlodging.application_services.users import UserService

fake = Faker()


@pytest.mark.django_db
class TestUserService:
    def test_create_succeeds(self):
        email = fake.email()
        password = fake.password()
        user = UserService.create(email=email, password=password)

        assert user is not None
        assert user.email == email
        assert user.password != password
        assert check_password(str(password), user.password) is True

    def test_create_with_short_numeric_password_fails(self):
        email = fake.email()
        password = fake.numerify("###")

        with pytest.raises(ValidationError) as ex:
            UserService.create(email=email, password=password)
        assert "This password is too short. It must contain at least 8 characters." in ex.value
        assert "This password is entirely numeric." in ex.value

    def test_create_with_short_similar_password_fails(self):
        email = fake.email()
        password = email[:-1]

        with pytest.raises(ValidationError) as ex:
            UserService.create(email=email, password=password)
        assert "The password is too similar to the email." in ex.value

    def test_create_with_common_password_fails(self):
        email = fake.email()
        password = "qwertyuiop"

        with pytest.raises(ValidationError) as ex:
            UserService.create(email=email, password=password)
        assert "This password is too common." in ex.value
