import pytest
from django.urls import reverse
from factory import Faker
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from tests.domain.users.factories import UserFactory


@pytest.mark.django_db
def test_user_login_with_fixtures_succeeds(api_client, user):
    url = reverse("users:user-login")  # "/api/users/login/"
    payload = {"email": user.email, "password": "1234"}
    response = api_client.post(url, payload)

    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_user_login_succeeds(api_client):
    password = Faker("password")
    user = UserFactory(password=password)
    user.set_password(str(password))
    user.save()
    url = reverse("users:user-login")  # "/api/users/login/"
    payload = {"email": user.email, "password": password}
    response = api_client.post(url, payload)

    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_user_login_with_wrong_email_fails(api_client):
    password = Faker("password")
    user = UserFactory(password=password)
    user.set_password(str(password))
    user.save()
    url = reverse("users:user-login")  # "/api/users/login/"
    payload = {"email": Faker("email"), "password": password}
    response = api_client.post(url, payload)

    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_login_with_wrong_password_fails(api_client):
    password = Faker("password")
    wrong_password = Faker("password")
    user = UserFactory(password=password)
    user.set_password(str(password))
    user.save()
    url = reverse("users:user-login")  # "/api/users/login/"
    payload = {"email": user.email, "password": wrong_password}
    response = api_client.post(url, payload)

    assert response.status_code == HTTP_401_UNAUTHORIZED
