from uuid import uuid4

import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.test import APIClient

from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestEmailChangeRequestAPIView:
    def test_request_email_change_succeeds(self, user_api_client_factory_boy):
        old_email = fake.email()
        new_email = fake.email()

        user = UserFactory(email=old_email)

        assert user.email == old_email

        payload = {"new_email": new_email}
        url = reverse("users:request-change-email")
        response = user_api_client_factory_boy.post(url, payload)

        assert response.status_code == HTTP_202_ACCEPTED

        user.refresh_from_db()
        assert user.email == old_email

    def test_request_email_change_without_new_email_fails(self, user_api_client_factory_boy):
        old_email = fake.email()
        user = UserFactory(email=old_email)

        assert user.email == old_email

        payload = {}
        url = reverse("users:request-change-email")
        response = user_api_client_factory_boy.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data)
            == "{'detail': {'new_email': [ErrorDetail(string='This field is required.', "
            "code='required')]}}"
        )

        user.refresh_from_db()
        assert user.email == old_email

    def test_request_email_change_with_invalid_email_fails(self, user_api_client_factory_boy):
        old_email = fake.email()
        user = UserFactory(email=old_email)

        assert user.email == old_email

        payload = {"new_email": "new_email@com"}
        url = reverse("users:request-change-email")
        response = user_api_client_factory_boy.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data)
            == "{'detail': {'new_email': [ErrorDetail(string='Enter a valid email address.', "
            "code='invalid')]}}"
        )
        user.refresh_from_db()
        assert user.email == old_email

    def test_request_email_change_by_logged_out_user_fails(self):
        old_email = fake.email()
        new_email = fake.email()
        user = UserFactory(email=old_email)

        assert user.email == old_email

        payload = {"new_email": new_email}
        url = reverse("users:request-change-email")
        client = APIClient()
        response = client.post(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == "Authentication credentials were not provided."
        user.refresh_from_db()
        assert user.email == old_email


@pytest.mark.django_db
class TestEmailChangeConfirmAPIView:
    def test_email_change_succeeds(self):
        old_email = fake.email()
        new_email = fake.email()
        user = UserFactory(email=old_email)
        security_token = user.security_token

        assert user.email == old_email

        payload = {"security_token": security_token, "new_email": new_email}
        url = reverse("users:confirm-change-email")
        client = APIClient()
        response = client.post(url, payload)

        assert response.status_code == HTTP_200_OK

        user.refresh_from_db()
        assert user.email == new_email
        assert user.security_token == ""

    def test_email_change_with_wrong_token_fails(self):
        old_email = fake.email()
        new_email = fake.email()
        user_security_token = uuid4()
        wrong_security_token = uuid4()

        user = UserFactory(email=old_email, security_token=user_security_token)

        assert user.email == old_email
        assert user.security_token == str(user_security_token)

        payload = {"security_token": wrong_security_token, "new_email": new_email}
        url = reverse("users:confirm-change-email")
        client = APIClient()
        response = client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'non_field_errors': [ErrorDetail(string='User does not exist', code='invalid')]}"
        )

        user.refresh_from_db()
        assert user.email == old_email
        assert user.security_token != ""

    def test_email_change_without_token_fails(self):
        old_email = fake.email()
        new_email = fake.email()

        user = UserFactory(email=old_email)

        assert user.email == old_email

        payload = {"new_email": new_email}
        url = reverse("users:confirm-change-email")
        client = APIClient()
        response = client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'security_token': [ErrorDetail(string='This field is required.', "
            "code='required')]}"
        )

        user.refresh_from_db()
        assert user.email == old_email
        assert user.security_token != ""

    def test_email_change_without_email_fails(self):
        old_email = fake.email()
        user = UserFactory(email=old_email)

        payload = {"security_token": user.security_token}
        url = reverse("users:confirm-change-email")
        client = APIClient()
        response = client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'new_email': [ErrorDetail(string='This field is required.', code='required')]}"
        )

        user.refresh_from_db()
        assert user.email == old_email
        assert user.security_token != ""

    def test_email_change_without_token_and_without_email_fails(self):
        old_email = fake.email()
        user = UserFactory(email=old_email)

        payload = {}
        url = reverse("users:confirm-change-email")
        client = APIClient()
        response = client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'security_token': [ErrorDetail(string='This field is required.', "
            "code='required')], 'new_email': [ErrorDetail(string='This field is required.', "
            "code='required')]}"
        )

        user.refresh_from_db()
        assert user.email == old_email
        assert user.security_token != ""

    def test_email_change_with_invalid_email_fails(self):
        old_email = fake.email()
        user_security_token = uuid4()

        user = UserFactory(email=old_email, security_token=user_security_token)

        assert user.email == old_email
        assert user.security_token == str(user_security_token)

        payload = {"security_token": user_security_token, "new_email": "new_email@com"}
        url = reverse("users:confirm-change-email")
        client = APIClient()
        response = client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'new_email': [ErrorDetail(string='Enter a valid email address.', "
            "code='invalid')]}"
        )

        user.refresh_from_db()
        assert user.email == old_email
        assert user.security_token != ""
