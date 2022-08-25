import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

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
        print(response.data)
        assert (
            str(response.data["detail"])
            == "{'non_field_errors': [ErrorDetail(string='Wrong password!', code='invalid')]}"
        )
        user.refresh_from_db()
        assert user.check_password(new_password) is False


@pytest.mark.django_db
class TestForgotPasswordAPIView:
    def test_forgot_password_succeeds(self):
        api_client = APIClient()
        user = UserFactory()

        security_token = user.security_token

        payload = {"email": user.email}

        url = reverse("users:forgot-password")
        response = api_client.post(url, payload)
        assert response.status_code == HTTP_202_ACCEPTED

        user.refresh_from_db()
        assert user.security_token != security_token
