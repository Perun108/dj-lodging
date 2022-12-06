from uuid import uuid4

import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from djlodging.domain.users.constants import USER_DOES_NOT_EXIST_MESSAGE
from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestPasswordChangeAPIView:
    def test_password_change_succeeds(self, user_api_client_pytest_fixture, user, password):
        new_password = fake.password()
        assert user.check_password(password) is True

        payload = {"old_password": password, "new_password": new_password}

        url = reverse("users:change-password")
        response = user_api_client_pytest_fixture.patch(url, payload)

        assert response.status_code == HTTP_200_OK

        user.refresh_from_db()
        assert user.check_password(password) is False
        assert user.check_password(new_password) is True

    def test_password_change_with_wrong_old_password_fails(
        self, user_api_client_pytest_fixture, user
    ):
        old_password = fake.password()
        new_password = fake.password()
        assert user.check_password(old_password) is False

        payload = {"old_password": old_password, "new_password": new_password}

        url = reverse("users:change-password")
        response = user_api_client_pytest_fixture.patch(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Wrong password!"
        user.refresh_from_db()
        assert user.check_password(new_password) is False


@pytest.mark.django_db
class TestSendForgotPasswordLinkAPIView:
    def test_forgot_password_succeeds(self, mocker):
        api_client = APIClient()
        user = UserFactory()

        security_token = user.security_token
        mock = mocker.patch(
            "djlodging.application_services.email.EmailService.send_change_password_link",
        )
        payload = {"email": user.email}

        url = reverse("users:forgot-password")
        response = api_client.post(url, payload)
        assert response.status_code == HTTP_202_ACCEPTED
        mock.assert_called_once()

        user.refresh_from_db()
        assert user.security_token != security_token


@pytest.mark.django_db
class TestPasswordResetConfirmAPIView:
    def test_reset_password_succeeds(self):
        api_client = APIClient()
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)
        security_token = user.security_token

        payload = {
            "security_token": security_token,
            "email": user.email,
            "new_password": new_password,
        }

        url = reverse("users:confirm-reset-password")
        response = api_client.post(url, payload)
        assert response.status_code == HTTP_200_OK

        user.refresh_from_db()

        assert user.check_password(old_password) is False
        assert user.check_password(new_password) is True
        assert user.security_token != security_token
        assert user.security_token == ""

    def test_reset_password_with_wrong_token_fails(self):
        api_client = APIClient()
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)
        security_token = user.security_token
        wrong_security_token = uuid4()

        payload = {
            "security_token": wrong_security_token,
            "email": user.email,
            "new_password": new_password,
        }

        url = reverse("users:confirm-reset-password")
        response = api_client.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["message"] == USER_DOES_NOT_EXIST_MESSAGE

        user.refresh_from_db()

        assert user.check_password(old_password) is True
        assert user.check_password(new_password) is False
        assert user.security_token == security_token

    def test_reset_password_with_wrong_email_fails(self):
        api_client = APIClient()
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)
        security_token = user.security_token
        wrong_email = fake.email()

        payload = {
            "security_token": security_token,
            "email": wrong_email,
            "new_password": new_password,
        }

        url = reverse("users:confirm-reset-password")
        response = api_client.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["message"] == USER_DOES_NOT_EXIST_MESSAGE

        user.refresh_from_db()

        assert user.check_password(old_password) is True
        assert user.check_password(new_password) is False
        assert user.security_token == security_token

    def test_reset_password_with_wrong_token_and_wrong_email_fails(self):
        api_client = APIClient()
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)
        security_token = user.security_token
        wrong_security_token = uuid4()
        wrong_email = fake.email()

        payload = {
            "security_token": wrong_security_token,
            "email": wrong_email,
            "new_password": new_password,
        }

        url = reverse("users:confirm-reset-password")
        response = api_client.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["message"] == USER_DOES_NOT_EXIST_MESSAGE

        user.refresh_from_db()

        assert user.check_password(old_password) is True
        assert user.check_password(new_password) is False
        assert user.security_token == security_token

    def test_reset_password_without_token_fails(self):
        api_client = APIClient()
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)

        payload = {
            "email": user.email,
            "new_password": new_password,
        }

        url = reverse("users:confirm-reset-password")
        response = api_client.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data)
            == "{'security_token': [ErrorDetail(string='This field is required.', "
            "code='required')]}"
        )

        user.refresh_from_db()

        assert user.check_password(old_password) is True
        assert user.check_password(new_password) is False
        assert user.security_token != ""

    def test_reset_password_without_email_fails(self):
        api_client = APIClient()
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)
        security_token = user.security_token

        payload = {
            "security_token": security_token,
            "new_password": new_password,
        }

        url = reverse("users:confirm-reset-password")
        response = api_client.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data) == "{'email': [ErrorDetail(string='This field is required.', "
            "code='required')]}"
        )

        user.refresh_from_db()

        assert user.check_password(old_password) is True
        assert user.check_password(new_password) is False
        assert user.security_token == security_token

    def test_reset_password_without_token_and_without_email_fails(self):
        api_client = APIClient()
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)

        payload = {
            "new_password": new_password,
        }

        url = reverse("users:confirm-reset-password")
        response = api_client.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data)
            == "{'security_token': [ErrorDetail(string='This field is required.', "
            "code='required')], 'email': [ErrorDetail(string='This field is required.', "
            "code='required')]}"
        )

        user.refresh_from_db()

        assert user.check_password(old_password) is True
        assert user.check_password(new_password) is False
        assert user.security_token != ""
