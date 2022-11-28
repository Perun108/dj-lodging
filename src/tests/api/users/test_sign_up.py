import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from djlodging.domain.users.models import User

fake = Faker()


@pytest.mark.django_db
class TestUserSingUpAPIView:
    def test_user_sign_up_succeeds(self, mocker):
        api_client = APIClient()
        email = fake.email()
        password = fake.password()

        mock = mocker.patch(
            "djlodging.application_services.email.EmailService.send_confirmation_link",
            return_value=None,
        )

        url = reverse("users:sign-up")  # "/api/users/sign-up/"
        payload = {"email": email, "password": password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_201_CREATED
        mock.assert_called_once()

        user = User.objects.first()
        assert user is not None
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
        assert (
            str(response.data)
            == "{'email': [ErrorDetail(string='This field is required.', code='required')]}"
        )

    def test_sign_up_without_password_fails(self):
        api_client = APIClient()
        email = fake.email()

        url = reverse("users:sign-up")  # "/api/users/sign-up/"
        payload = {"email": email}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data)
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
            str(response.data)
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
            str(response.data)
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
            str(response.data)
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
        assert (
            str(response.data)
            == "{'email': [ErrorDetail(string='Enter a valid email address.', code='invalid')]}"
        )
