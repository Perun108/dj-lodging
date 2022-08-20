from uuid import uuid4

import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.test import APIClient

from djlodging.domain.users.models import User
from tests.domain.users.factories import UserFactory

fake = Faker()


# @pytest.mark.usefixtures("api_client")
@pytest.mark.django_db
class TestUserSingUpAPIView:
    def test_user_sign_up_succeeds(self):
        api_client = APIClient()
        # original_count = User.objects.count()
        email = fake.email()
        password = fake.password()

        url = reverse("users:sign-up")  # "/api/users/sign-up/"
        payload = {"email": email, "password": password}
        response = api_client.post(url, payload)

        # count = User.objects.count()
        # user = User.objects.filter(email=email).first()
        assert response.status_code == HTTP_201_CREATED

        user = User.objects.first()
        assert user is not None
        # assert count == original_count + 1
        assert user.email == email
        assert user.is_active is False
        assert user.is_user is True
        assert user.is_partner is False
        assert user.is_staff is False

    def test_sign_up_without_email_fails(self):
        api_client = APIClient()
        password = fake.password()

        url = reverse("users:sign-up")  # "/api/users/sign-up/"
        payload = {"password": password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "email" in response.data["detail"]
        assert (
            str(response.data["detail"])
            == "{'email': [ErrorDetail(string='This field is required.', code='required')]}"
        )

    def test_sign_up_without_password_fails(self):
        api_client = APIClient()
        email = fake.email()

        url = reverse("users:sign-up")  # "/api/users/sign-up/"
        payload = {"email": email}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "password" in response.data["detail"]
        assert (
            str(response.data["detail"])
            == "{'password': [ErrorDetail(string='This field is required.', code='required')]}"
        )

    def test_sign_up_with_weak_similar_password_fails(self):
        api_client = APIClient()
        email = fake.email()
        password = email[1:-1]

        url = reverse("users:sign-up")  # "/api/users/sign-up/"
        payload = {"email": email, "password": password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'non_field_errors': [ErrorDetail(string='The password is too similar to the email.', code='password_too_similar')]}"  # noqa
        )

    def test_sign_up_with_weak_common_password_fails(self):
        api_client = APIClient()
        email = fake.email()
        password = "qwertyuiop"

        url = reverse("users:sign-up")  # "/api/users/sign-up/"
        payload = {"email": email, "password": password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'non_field_errors': [ErrorDetail(string='This password is too common.', code='password_too_common')]}"  # noqa
        )

    def test_sign_up_with_weak_numeric_password_fails(self):
        api_client = APIClient()
        email = fake.email()
        password = "1234567890"

        url = reverse("users:sign-up")  # "/api/users/sign-up/"
        payload = {"email": email, "password": password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'non_field_errors': [ErrorDetail(string='This password is too common.', "
            "code='password_too_common'), ErrorDetail(string='This password is entirely numeric.',"
            " code='password_entirely_numeric')]}"
        )

    def test_sign_up_with_invalid_email_fails(self):
        api_client = APIClient()
        invalid_email = f"{fake.first_name()}@com"
        password = fake.password()

        url = reverse("users:sign-up")  # "/api/users/sign-up/"
        payload = {"email": invalid_email, "password": password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "email" in response.data["detail"]
        assert (
            str(response.data["detail"])
            == "{'email': [ErrorDetail(string='Enter a valid email address.', code='invalid')]}"
        )


@pytest.mark.django_db
class TestUserRegistrationConfirmAPIView:
    def test_confirm_registration_succeeds(self):
        api_client = APIClient()
        user = UserFactory(is_active=False)
        assert user.is_active is False
        assert user.registration_token != ""

        url = reverse("users:registration")
        payload = {"registration_token": user.registration_token}

        response = api_client.post(url, payload)
        assert response.status_code == HTTP_200_OK

        user.refresh_from_db()
        assert user.is_active is True
        assert user.registration_token == ""
        assert response.data["id"] == str(user.id)
        assert response.data["email"] == user.email

    def test_confirm_registration_without_registration_token_fails(self):
        api_client = APIClient()
        user = UserFactory(is_active=False)
        assert user.registration_token != ""
        assert user.is_active is False

        url = reverse("users:registration")
        payload = {"registration_token": ""}

        response = api_client.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST

        user.refresh_from_db()
        assert user.is_active is False
        assert user.registration_token != ""

    def test_confirm_registration_with_wrong_registration_token_fails(self):
        api_client = APIClient()
        user = UserFactory(is_active=False)
        wrong_token = uuid4()
        assert user.registration_token != wrong_token
        assert user.is_active is False

        url = reverse("users:registration")
        payload = {"registration_token": wrong_token}

        response = api_client.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data)
            == "{'detail': {'non_field_errors': [ErrorDetail(string='Such user does not exist', "
            "code='invalid')]}}"
        )
        user.refresh_from_db()
        assert user.is_active is False
        assert user.registration_token != ""


@pytest.mark.django_db
class TestUserLoginAPIView:
    def test_user_login_with_fixtures_succeeds(self, user, password):
        api_client = APIClient()
        url = reverse("users:login")  # "/api/users/login/"
        payload = {"email": user.email, "password": password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_200_OK
        assert response.data["user_id"] == user.id
        assert response.data["is_user"] is True
        assert response.data["is_partner"] is False

    def test_user_login_with_factory_succeeds(self):
        api_client = APIClient()
        raw_password = fake.password()
        user = UserFactory(password=raw_password)
        url = reverse("users:login")  # "/api/users/login/"
        payload = {"email": user.email, "password": raw_password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_200_OK
        assert response.data["user_id"] == user.id
        assert response.data["is_user"] is True
        assert response.data["is_partner"] is False

    def test_user_login_with_wrong_email_fails(self):
        api_client = APIClient()
        raw_password = fake.password()
        user = UserFactory(password=raw_password)  # noqa
        url = reverse("users:login")  # "/api/users/login/"
        payload = {"email": fake.email(), "password": raw_password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_user_login_with_wrong_password_fails(self):
        api_client = APIClient()
        wrong_password = fake.password()
        user = UserFactory()
        url = reverse("users:login")  # "/api/users/login/"
        payload = {"email": user.email, "password": wrong_password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_inactive_user_login_fails(self):
        api_client = APIClient()
        raw_password = fake.password()
        user = UserFactory(password=raw_password, is_active=False)

        url = reverse("users:login")  # "/api/users/login/"
        payload = {"email": user.email, "password": raw_password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED


# # class TestUserViewSet:
