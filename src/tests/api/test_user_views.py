from uuid import uuid4

import pytest
from django.core.exceptions import ValidationError as DjangoValidationError
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from djlodging.domain.users.models import User
from tests.domain.users.factories import UserFactory

fake = Faker()


# @pytest.mark.usefixtures("api_client")
@pytest.mark.django_db
class TestUserSingUpAPIView:
    def test_user_sign_up_succeeds(self, api_client):
        original_count = User.objects.count()

        email = fake.email()
        password = fake.password()

        url = reverse("users:sign-up")  # "/api/users/sign-up/"
        payload = {"email": email, "password": password}
        response = api_client.post(url, payload)

        count = User.objects.count()
        user = User.objects.filter(email=email).first()

        assert response.status_code == HTTP_201_CREATED
        assert user is not None
        assert count == original_count + 1
        assert user.is_active is False

    def test_user_create_without_email_fails(self, api_client):
        password = fake.password()

        url = reverse("users:sign-up")  # "/api/users/sign-up/"
        payload = {"password": password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data)
            == "{'email': [ErrorDetail(string='This field is required.', code='required')]}"
        )

    def test_user_create_without_password_fails(self, api_client):
        email = fake.email()

        url = reverse("users:sign-up")  # "/api/users/sign-up/"
        payload = {"email": email}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data)
            == "{'password': [ErrorDetail(string='This field is required.', code='required')]}"
        )

    def test_user_create_with_invalid_email_fails(self, api_client):
        invalid_email = f"{fake.first_name()}@com"
        password = fake.password()

        url = reverse("users:sign-up")  # "/api/users/sign-up/"
        payload = {"email": invalid_email, "password": password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data)
            == "{'email': [ErrorDetail(string='Enter a valid email address.', code='invalid')]}"
        )


@pytest.mark.django_db
class TestUserRegistrationConfirmAPIView:
    def test_confirm_registration_succeeds(self, api_client):
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

    def test_confirm_registration_without_token_fails(self, api_client):
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

    def test_confirm_registration_with_wrong_token_fails(self, api_client):
        user = UserFactory(is_active=False)
        wrong_token = uuid4()
        assert user.registration_token != wrong_token
        assert user.is_active is False

        url = reverse("users:registration")
        payload = {"registration_token": wrong_token}

        with pytest.raises(DjangoValidationError) as exc:
            response = api_client.post(url, payload)
            assert response.status_code == HTTP_400_BAD_REQUEST
        assert "Such user does not exist" in exc.value

        user.refresh_from_db()
        assert user.is_active is False
        assert user.registration_token != ""


@pytest.mark.django_db
class TestUserLoginAPIView:
    def test_user_login_with_fixtures_succeeds(self, api_client, user, password):
        url = reverse("users:login")  # "/api/users/login/"
        payload = {"email": user.email, "password": password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_200_OK

    def test_user_login_succeeds(self, api_client):
        raw_password = fake.password()
        user = UserFactory(password=raw_password)
        url = reverse("users:login")  # "/api/users/login/"
        payload = {"email": user.email, "password": raw_password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_200_OK

    def test_user_login_with_wrong_email_fails(self, api_client):
        raw_password = fake.password()
        user = UserFactory(password=raw_password)  # noqa
        url = reverse("users:login")  # "/api/users/login/"
        payload = {"email": fake.email(), "password": raw_password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_user_login_with_wrong_password_fails(self, api_client):
        wrong_password = fake.password()
        user = UserFactory()
        url = reverse("users:login")  # "/api/users/login/"
        payload = {"email": user.email, "password": wrong_password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_inactive_user_login_fails(self, api_client):
        raw_password = fake.password()
        user = UserFactory(password=raw_password, is_active=False)

        url = reverse("users:login")  # "/api/users/login/"
        payload = {"email": user.email, "password": raw_password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED


# # class TestUserViewSet:
