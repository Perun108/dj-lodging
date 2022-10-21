import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient

fake = Faker()


@pytest.mark.django_db
class TestMeViewSet:
    def test_make_me_partner_succeeds(self, user_api_client_pytest_fixture, user):
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone_number = "+16478081020"

        assert user.is_partner is False
        assert user.first_name != first_name
        assert user.last_name != last_name
        assert user.phone_number != phone_number

        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
        }
        url = reverse("me-create-partner")
        response = user_api_client_pytest_fixture.patch(url, payload)

        assert response.status_code == HTTP_200_OK
        assert response.data["id"] == str(user.id)

        user.refresh_from_db()
        assert user.is_partner is True
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.phone_number == phone_number

    def test_make_me_partner_by_not_logged_user_fails(self):
        api_client = APIClient()

        first_name = fake.first_name()
        last_name = fake.last_name()
        phone_number = "+16478081020"

        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
        }
        url = reverse("me-create-partner")
        response = api_client.patch(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == "Authentication credentials were not provided."
