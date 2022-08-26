from uuid import uuid4

import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from djlodging.domain.users.models import PaymentProviderUser
from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestUserRegistrationConfirmAPIView:
    def test_confirm_registration_succeeds(self):
        api_client = APIClient()
        user = UserFactory(is_active=False)
        assert user.is_active is False
        assert user.security_token != ""

        assert PaymentProviderUser.objects.first() is None

        url = reverse("users:registration")
        payload = {"security_token": user.security_token}

        response = api_client.post(url, payload)
        assert response.status_code == HTTP_200_OK

        user.refresh_from_db()
        assert user.is_active is True
        assert user.security_token == ""
        assert response.data["id"] == str(user.id)
        assert response.data["email"] == user.email

        payment_user = PaymentProviderUser.objects.first()

        assert payment_user is not None
        assert payment_user.user == user

    def test_confirm_registration_without_security_token_fails(self):
        api_client = APIClient()
        user = UserFactory(is_active=False)
        assert user.security_token != ""
        assert user.is_active is False

        url = reverse("users:registration")
        payload = {"security_token": ""}

        response = api_client.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST

        user.refresh_from_db()
        assert user.is_active is False
        assert user.security_token != ""

    def test_confirm_registration_with_wrong_security_token_fails(self):
        api_client = APIClient()
        user = UserFactory(is_active=False)
        wrong_token = uuid4()
        assert user.security_token != wrong_token
        assert user.is_active is False

        url = reverse("users:registration")
        payload = {"security_token": wrong_token}

        response = api_client.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data)
            == "{'detail': {'non_field_errors': [ErrorDetail(string='Such user does not exist', "
            "code='invalid')]}}"
        )
        user.refresh_from_db()
        assert user.is_active is False
        assert user.security_token != ""
