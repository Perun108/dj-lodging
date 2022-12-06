from uuid import uuid4

import pytest
from django.utils.timezone import now, timedelta
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from djlodging.domain.users.constants import USER_DOES_NOT_EXIST_OR_WAS_DELETED_MESSAGE
from djlodging.domain.users.models import PaymentProviderUser
from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestUserRegistrationConfirmAPIView:
    def test_confirm_registration_succeeds(self, mocker):
        api_client = APIClient()
        security_token_expiration_time = now() + timedelta(hours=2)
        user = UserFactory(
            is_active=False, security_token_expiration_time=security_token_expiration_time
        )

        assert user.is_active is False
        assert user.security_token != ""
        assert user.security_token_expiration_time > now()
        assert PaymentProviderUser.objects.first() is None

        mock = mocker.patch(
            "djlodging.application_services.users.PaymentProviderUserService.create"
        )

        url = reverse("users:registration")
        payload = {"user_id": user.id, "security_token": user.security_token}

        response = api_client.post(url, payload)
        assert response.status_code == HTTP_200_OK
        mock.assert_called_once()

        user.refresh_from_db()
        assert user.is_active is True
        assert user.security_token == ""
        assert response.data is None

        # TODO Move these check to application_services tests
        # payment_user = PaymentProviderUser.objects.first()

        # assert payment_user is not None
        # assert payment_user.user == user

    def test_confirm_registration_without_security_token_fails(self):
        api_client = APIClient()
        user = UserFactory(is_active=False)
        assert user.security_token != ""
        assert user.is_active is False

        url = reverse("users:registration")
        payload = {"security_token": ""}

        response = api_client.post(url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data)
            == "{'user_id': [ErrorDetail(string='This field is required.', code='required')], "
            "'security_token': [ErrorDetail(string='Must be a valid UUID.', code='invalid')]}"
        )

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
        payload = {"user_id": user.id, "security_token": wrong_token}

        response = api_client.post(url, payload)
        assert response is not None
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["message"] == USER_DOES_NOT_EXIST_OR_WAS_DELETED_MESSAGE

        user.refresh_from_db()
        assert user.is_active is False
        assert user.security_token != ""
