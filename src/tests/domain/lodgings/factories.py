from django.contrib.auth import get_user_model
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

# from faker import Faker as Fake
from djlodging.domain.lodgings.models import Country
from djlodging.domain.lodgings.models.city import City

User = get_user_model()
# fake = Fake()


class CountryFactory(DjangoModelFactory):
    name = Faker("country")

    class Meta:
        model = Country


class CityFactory(DjangoModelFactory):
    name = Faker("city")
    country = SubFactory(CountryFactory)

    class Meta:
        model = City
