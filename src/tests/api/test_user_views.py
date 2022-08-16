import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from djbooking.domain.users.models import User
from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
def test_user_login_with_fixtures_succeeds(api_client, user):
    url = reverse("users:user-login")  # "/api/users/login/"
    payload = {"email": user.email, "password": "1234"}
    response = api_client.post(url, payload)

    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_user_login_succeeds(api_client):
    password = fake.password()
    user = UserFactory(password=password)
    user.set_password(password)
    user.save()
    url = reverse("users:user-login")  # "/api/users/login/"
    payload = {"email": user.email, "password": password}
    response = api_client.post(url, payload)

    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_user_login_with_wrong_email_fails(api_client):
    password = fake.password()
    user = UserFactory(password=password)
    user.set_password(password)
    user.save()
    url = reverse("users:user-login")  # "/api/users/login/"
    payload = {"email": fake.email(), "password": password}
    response = api_client.post(url, payload)

    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_login_with_wrong_password_fails(api_client):
    password = fake.password()
    wrong_password = fake.password()
    user = UserFactory(password=password)
    user.set_password(password)
    user.save()
    url = reverse("users:user-login")  # "/api/users/login/"
    payload = {"email": user.email, "password": wrong_password}
    response = api_client.post(url, payload)

    assert response.status_code == HTTP_401_UNAUTHORIZED


# @pytest.mark.usefixtures("api_client")
@pytest.mark.django_db
class TestUserViewSet:
    def test_user_create_succeeds(self, api_client):
        original_count = User.objects.count()

        email = fake.email()
        password = fake.password()

        url = reverse("user-list")  # "/api/users/"
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

        url = reverse("user-list")  # "/api/users/"
        payload = {"password": password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data)
            == "{'email': [ErrorDetail(string='This field is required.', code='required')]}"
        )

    def test_user_create_without_password_fails(self, api_client):
        email = fake.email()

        url = reverse("user-list")  # "/api/users/"
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

        url = reverse("user-list")  # "/api/users/"
        payload = {"email": invalid_email, "password": password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data)
            == "{'email': [ErrorDetail(string='Enter a valid email address.', code='invalid')]}"
        )
