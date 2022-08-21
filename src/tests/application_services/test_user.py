import pytest
from django.contrib.auth.hashers import check_password
from django.core.exceptions import PermissionDenied, ValidationError
from faker import Faker

from djlodging.application_services.users import UserService
from tests.domain.users.factories import UserFactory

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

    def test_make_user_partner_by_the_same_user_succeeds(self):
        user = UserFactory()
        assert user.is_partner is False

        first_name = fake.first_name()
        last_name = fake.last_name()
        # We use a hard-coded phone number because Faker generates very long phone numbers.
        phone_number = "+16478081020"
        partner = UserService.make_user_partner(
            actor=user,
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )

        user.refresh_from_db()

        assert partner.is_partner is True
        assert user.is_partner is True
        assert partner == user
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.phone_number == phone_number

    def test_make_user_partner_by_another_user_fails(self):
        actor = UserFactory()
        user = UserFactory()
        assert user.is_partner is False

        first_name = fake.first_name()
        last_name = fake.last_name()
        # We use a hard-coded phone number because Faker generates very long phone numbers.
        phone_number = "+16478081020"

        with pytest.raises(PermissionDenied):
            UserService.make_user_partner(
                actor=actor,
                user_id=user.id,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
            )

        user.refresh_from_db()

        assert user.is_partner is False
        assert user.first_name != first_name
        assert user.last_name != last_name
        assert user.phone_number != phone_number
