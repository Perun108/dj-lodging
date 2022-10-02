import pytest
from django.utils import timezone
from faker import Faker
from pytest_django.asserts import assertQuerysetEqual

from djlodging.domain.lodgings.repositories import LodgingRepository
from tests.domain.bookings.factories import BookingFactory
from tests.domain.lodgings.factories import CityFactory, LodgingFactory

fake = Faker()


@pytest.mark.django_db
def test_get_list_with_available_and_unavailable_for_same_dates_succeeds():
    number_of_lodgings = 5
    number_of_bookings = 3

    city = CityFactory()
    number_of_people = 1
    number_of_rooms = 1

    dates_from_list = [
        timezone.now().date() + timezone.timedelta(days=day) for day in range(number_of_bookings)
    ]

    available_only = False

    # Create lodgings
    lodgings = LodgingFactory.create_batch(size=number_of_lodgings, city=city)

    # Book some lodgings for some dates starting from today and adding the default 3 days.
    # Thus we will have {number_of_bookings} bookings and
    # {number_of_lodgings - number_of_bookings} available lodgings.
    for i in range(number_of_bookings):
        BookingFactory(lodging=lodgings[i], date_from=dates_from_list[i])

    # Get list of all lodgings for a range from today till the last booked date.
    date_from = timezone.now().date()
    date_to = date_from + timezone.timedelta(days=number_of_bookings)

    lodgings = LodgingRepository.get_list(
        date_from=date_from,
        date_to=date_to,
        number_of_people=number_of_people,
        number_of_rooms=number_of_rooms,
        city=city,
        available_only=available_only,
    )

    assert lodgings.count() == number_of_lodgings
    assert lodgings.filter(available=False).count() == number_of_bookings
    assert lodgings.filter(available=True).count() == number_of_lodgings - number_of_bookings


@pytest.mark.django_db
def test_get_list_with_available_and_unavailable_for_different_dates_succeeds():
    number_of_lodgings = 4
    number_of_bookings = 2

    city = CityFactory()
    number_of_people = 1
    number_of_rooms = 1

    dates_from_list = [
        timezone.now().date() + timezone.timedelta(days=day) for day in range(number_of_bookings)
    ]

    available_only = False

    # Create lodgings
    lodgings = LodgingFactory.create_batch(size=number_of_lodgings, city=city)

    # Book some lodgings for some dates starting from today and adding the default 3 days.
    # Thus we will have {number_of_bookings} bookings and
    # {number_of_lodgings - number_of_bookings} available lodgings.
    for i in range(number_of_bookings):
        BookingFactory(lodging=lodgings[i], date_from=dates_from_list[i])

    # Get list of all lodgings for a range completely different from the booked dates.
    date_from = timezone.now().date() + timezone.timedelta(days=30)
    date_to = date_from + timezone.timedelta(days=7)

    lodgings = LodgingRepository.get_list(
        date_from=date_from,
        date_to=date_to,
        number_of_people=number_of_people,
        number_of_rooms=number_of_rooms,
        city=city,
        available_only=available_only,
    )

    assert lodgings.count() == number_of_lodgings
    assert lodgings.filter(available=False).count() == 0
    assertQuerysetEqual(lodgings.filter(available=True), lodgings, ordered=False)


@pytest.mark.django_db
def test_get_list_with_only_available_for_same_dates_succeeds():
    number_of_lodgings = 5
    number_of_bookings = 3

    city = CityFactory()
    number_of_people = 1
    number_of_rooms = 1

    dates_from_list = [
        timezone.now().date() + timezone.timedelta(days=day) for day in range(number_of_bookings)
    ]

    available_only = True

    # Create lodgings
    lodgings = LodgingFactory.create_batch(size=number_of_lodgings, city=city)

    # Book some lodgings for some dates starting from today and adding the default 3 days.
    # Thus we will have {number_of_bookings} bookings and
    # {number_of_lodgings - number_of_bookings} available lodgings.
    for i in range(number_of_bookings):
        BookingFactory(lodging=lodgings[i], date_from=dates_from_list[i])

    # Get list of all lodgings for a range from today till the last booked date.
    date_from = timezone.now().date()
    date_to = date_from + timezone.timedelta(days=number_of_bookings)

    lodgings = LodgingRepository.get_list(
        date_from=date_from,
        date_to=date_to,
        number_of_people=number_of_people,
        number_of_rooms=number_of_rooms,
        city=city,
        available_only=available_only,
    )

    assert lodgings.count() == number_of_lodgings - number_of_bookings


@pytest.mark.django_db
def test_get_list_with_only_available__for_different_dates_succeeds():
    number_of_lodgings = 5
    number_of_bookings = 3

    city = CityFactory()
    number_of_people = 1
    number_of_rooms = 1

    dates_from_list = [
        timezone.now().date() + timezone.timedelta(days=day) for day in range(number_of_bookings)
    ]

    available_only = True

    # Create lodgings
    lodgings = LodgingFactory.create_batch(size=number_of_lodgings, city=city)

    # Book some lodgings for some dates starting from today and adding the default 3 days.
    # Thus we will have {number_of_bookings} bookings and
    # {number_of_lodgings - number_of_bookings} available lodgings.
    for i in range(number_of_bookings):
        BookingFactory(lodging=lodgings[i], date_from=dates_from_list[i])

    # Get list of all lodgings for a range completely different from the booked dates.
    date_from = timezone.now().date() + timezone.timedelta(days=30)
    date_to = date_from + timezone.timedelta(days=7)

    lodgings = LodgingRepository.get_list(
        date_from=date_from,
        date_to=date_to,
        number_of_people=number_of_people,
        number_of_rooms=number_of_rooms,
        city=city,
        available_only=available_only,
    )

    assert lodgings.count() == number_of_lodgings
