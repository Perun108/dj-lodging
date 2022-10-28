import pytest
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
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
            user=user,
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

    @staticmethod
    def test_change_password_succeeds():
        old_password = fake.password()
        user = UserFactory(password=old_password)
        new_password = fake.password()
        assert user.check_password(old_password) is True

        changed_user = UserService.change_password(
            user, old_password=old_password, new_password=new_password
        )
        assert changed_user.check_password(new_password) is True

        user.refresh_from_db()
        assert user.check_password(new_password) is True
        assert user.check_password(old_password) is False
        assert changed_user == user

    @staticmethod
    def test_change_password_with_wrong_old_password_fails():
        old_password = fake.password()
        user = UserFactory()
        new_password = fake.password()
        assert user.check_password(old_password) is False

        with pytest.raises(ValidationError) as exc:
            UserService.change_password(user, old_password=old_password, new_password=new_password)
        assert str(exc.value) == "['Wrong password!']"

        user.refresh_from_db()
        assert user.check_password(new_password) is False
        assert user.check_password(old_password) is False

    @staticmethod
    def test_send_forgot_password_link_succeeds(mocker):
        user = UserFactory()
        security_token = user.security_token

        mocker.patch(
            "djlodging.application_services.email.EmailService.send_change_password_link",
        )
        UserService.send_forgot_password_link(email=user.email)

        user.refresh_from_db()
        assert user.security_token != security_token

    @staticmethod
    def test_send_forgot_password_link_with_wrong_email_fails():
        user = UserFactory()
        wrong_email = fake.email()

        security_token = user.security_token

        with pytest.raises(ValidationError) as exc:
            UserService.send_forgot_password_link(email=wrong_email)
        assert str(exc.value) == "['Wrong email!']"

        user.refresh_from_db()
        assert user.security_token == security_token
