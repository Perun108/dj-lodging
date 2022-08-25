import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient

from tests.domain.users.factories import UserFactory

fake = Faker()


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
