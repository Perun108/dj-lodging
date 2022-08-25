import random

from django.contrib.auth import get_user_model
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker as Fake

from djlodging.domain.lodgings.models import City, Country, Lodging
from tests.domain.users.factories import UserFactory

User = get_user_model()
fake = Fake()


class CountryFactory(DjangoModelFactory):
    name = Faker("country")

    class Meta:
        model = Country


class CityFactory(DjangoModelFactory):
    name = Faker("city")
    country = SubFactory(CountryFactory)

    class Meta:
        model = City


class LodgingFactory(DjangoModelFactory):
    name = Faker("word")
    type = random.choice(Lodging.Type.choices)
    owner = SubFactory(UserFactory)
    city = SubFactory(CityFactory)
    street = Faker("street_name")
    house_number = Faker("building_number")
    zip_code = Faker("postcode")
    email = Faker("email")
    phone_number = Faker("phone_number")
    price = fake.numerify("###")

    class Meta:
        model = Lodging
