from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory

# from faker import Faker as Fake
from djlodging.domain.lodgings.models import Country

User = get_user_model()
# fake = Fake()


class CountryFactory(DjangoModelFactory):
    name = Faker("country")

    class Meta:
        model = Country
