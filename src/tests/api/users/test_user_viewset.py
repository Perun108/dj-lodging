import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestUserViewSet:
    def test_partner_by_same_user_succeeds(self, user_api_client_pytest_fixture, user):
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
        url = reverse("users-partner", args=[str(user.id)])
        response = user_api_client_pytest_fixture.patch(url, payload)

        assert response.status_code == HTTP_200_OK
        assert response.data["id"] == str(user.id)

        user.refresh_from_db()
        assert user.is_partner is True
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.phone_number == phone_number

    def test_partner_by_another_user_fails(self, user_api_client_pytest_fixture):
        user = UserFactory()

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
        url = reverse("users-partner", args=[str(user.id)])
        response = user_api_client_pytest_fixture.patch(url, payload)

        assert response.status_code == HTTP_403_FORBIDDEN
        assert str(response.data["detail"]) == "You do not have permission to perform this action."

        user.refresh_from_db()
        assert user.is_partner is False
        assert user.first_name != first_name
        assert user.last_name != last_name
        assert user.phone_number != phone_number
