import pytest

from djlodging.domain.lodgings.models import Country


@pytest.fixture
def country():
    name = "Some new country"
    country = Country.objects.create(name=name)
    country.save()
    return country
