from uuid import uuid4

import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestEmailChangeConfirmAPIView:
    def test_email_change_succeeds(self):
        old_email = fake.email()
        new_email = fake.email()

        user = UserFactory(email=old_email)

        assert user.email == old_email

        payload = {"security_token": user.security_token, "new_email": new_email}
        url = reverse("users:request-change-email")
        client = APIClient()
        response = client.post(url, payload)

        assert response.status_code == HTTP_200_OK

        user.refresh_from_db()
        assert user.email == new_email

    def test_email_change_with_wrong_token_fails(self):
        old_email = fake.email()
        new_email = fake.email()
        user_security_token = uuid4()
        wrong_security_token = uuid4()

        user = UserFactory(email=old_email, security_token=user_security_token)

        assert user.email == old_email
        assert user.security_token == str(user_security_token)

        payload = {"security_token": wrong_security_token, "new_email": new_email}
        url = reverse("users:request-change-email")
        client = APIClient()
        response = client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["detail"])
            == "{'non_field_errors': [ErrorDetail(string='User does not exist', code='invalid')]}"
        )

        user.refresh_from_db()
        assert user.email == old_email
