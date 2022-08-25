from django.contrib.auth import get_user_model
from django.utils import timezone
from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker as Fake

from djlodging.domain.bookings.models import Booking
from tests.domain.lodgings.factories import LodgingFactory
from tests.domain.users.factories import UserFactory

User = get_user_model()
fake = Fake()


class BookingFactory(DjangoModelFactory):
    lodging = SubFactory(LodgingFactory)
    user = SubFactory(UserFactory)
    date_from = timezone.now().date()
    date_to = date_from + timezone.timedelta(days=3)

    class Meta:
        model = Booking
