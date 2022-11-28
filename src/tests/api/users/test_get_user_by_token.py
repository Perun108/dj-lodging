import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from djlodging.domain.users.constants import USER_DOES_NOT_EXIST_MESSAGE
from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestUserGetByTokenAndEmailAPIView:
    def test_get_user_id_by_token_and_email_succeeds(self):
        user = UserFactory()

        query_params = {"token": user.security_token, "email": user.email}
        url = reverse("users:get-user-id")
        client = APIClient()
        response = client.get(url, query_params)

        assert response.status_code == HTTP_200_OK
        assert response.data == {"user_id": user.id}

    def test_get_user_id_by_token_and_email_without_token_fails(self):
        user = UserFactory()

        query_params = {"email": user.email}
        url = reverse("users:get-user-id")
        client = APIClient()
        response = client.get(url, query_params)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert str(response.data["message"]) == USER_DOES_NOT_EXIST_MESSAGE

    def test_get_user_id_by_token_and_email_without_email_fails(self):
        user = UserFactory()

        query_params = {"token": user.security_token}
        url = reverse("users:get-user-id")
        client = APIClient()
        response = client.get(url, query_params)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert str(response.data["message"]) == USER_DOES_NOT_EXIST_MESSAGE

    def test_get_user_id_by_token_and_email_without_token_and_email_fails(self):
        query_params = {}
        url = reverse("users:get-user-id")
        client = APIClient()
        response = client.get(url, query_params)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert str(response.data["message"]) == USER_DOES_NOT_EXIST_MESSAGE
