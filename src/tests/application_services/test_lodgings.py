import pytest
from django.core.exceptions import PermissionDenied
from faker import Faker

from djlodging.application_services.lodgings import CityService
from tests.domain.lodgings.factories import CountryFactory
from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestCityService:
    def test_create_city_by_admin_succeeds(self):
        actor = UserFactory(is_staff=True)
        country = CountryFactory()

        name = fake.name()
        city = CityService.create(actor=actor, country_id=country.id, name=name)

        assert city is not None
        assert city.country == country
        assert city.country.name == country.name
        assert city.name == name

    def test_create_city_by_user_fails(self):
        actor = UserFactory(is_staff=False)
        country = CountryFactory()

        name = fake.name()
        with pytest.raises(PermissionDenied):
            CityService.create(actor=actor, country_id=country.id, name=name)
