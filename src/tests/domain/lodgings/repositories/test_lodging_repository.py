import pytest
from django.db.models import Avg
from django.db.models.functions import Round
from django.utils import timezone
from faker import Faker
from pytest_django.asserts import assertQuerysetEqual

from djlodging.domain.lodgings.models.review import Review
from djlodging.domain.lodgings.repositories import LodgingRepository
from tests.domain.bookings.factories import BookingFactory
from tests.domain.lodgings.factories import CityFactory, LodgingFactory, ReviewFactory

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

    # Create reviews for one of the lodgings to get average_rating
    number_of_reviews = 4
    ReviewFactory.create_batch(size=number_of_reviews, lodging=lodgings[0])
    average_reviews_rating = Review.objects.aggregate(
        average_rating=Round(Avg("score"), precision=1)
    )["average_rating"]

    # Get list of all lodgings for a range from today till the last booked date.
    date_from = timezone.now().date()
    date_to = date_from + timezone.timedelta(days=number_of_bookings)

    result = LodgingRepository.get_list(
        date_from=date_from,
        date_to=date_to,
        number_of_people=number_of_people,
        number_of_rooms=number_of_rooms,
        city=city,
        available_only=available_only,
    )

    assert result.count() == number_of_lodgings
    assert result.filter(available=False).count() == number_of_bookings
    assert result.filter(available=True).count() == number_of_lodgings - number_of_bookings

    # Get the reviewed lodging and assert for its average_rating
    reviewed_lodging = result.get(id=lodgings[0].id)
    assert reviewed_lodging.average_rating == average_reviews_rating

    # Assert that other (not reviewed) lodgings have no average_rating
    for lodging in result.exclude(id=lodgings[0].id):
        assert lodging.average_rating is None


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

    # Create reviews for one of the lodgings to get average_rating
    number_of_reviews = 4
    ReviewFactory.create_batch(size=number_of_reviews, lodging=lodgings[0])
    average_reviews_rating = Review.objects.aggregate(
        average_rating=Round(Avg("score"), precision=1)
    )["average_rating"]

    # Get list of all lodgings for a range completely different from the booked dates.
    date_from = timezone.now().date() + timezone.timedelta(days=30)
    date_to = date_from + timezone.timedelta(days=7)

    result = LodgingRepository.get_list(
        date_from=date_from,
        date_to=date_to,
        number_of_people=number_of_people,
        number_of_rooms=number_of_rooms,
        city=city,
        available_only=available_only,
    )

    assert result.count() == number_of_lodgings
    assert result.filter(available=False).count() == 0
    assertQuerysetEqual(result.filter(available=True), result, ordered=False)

    # Get the reviewed lodging and assert for its average_rating
    reviewed_lodging = result.get(id=lodgings[0].id)
    assert reviewed_lodging.average_rating == average_reviews_rating

    # Assert that other (not reviewed) lodgings have no average_rating
    for lodging in result.exclude(id=lodgings[0].id):
        assert lodging.average_rating is None


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

    # Create reviews for the unbooked lodging to get average_rating
    # since booked lodgings should not be returned in this method call under test.
    number_of_reviews = 4
    ReviewFactory.create_batch(size=number_of_reviews, lodging=lodgings[number_of_bookings])
    average_reviews_rating = Review.objects.aggregate(
        average_rating=Round(Avg("score"), precision=1)
    )["average_rating"]

    # Get list of all lodgings for a range from today till the last booked date.
    date_from = timezone.now().date()
    date_to = date_from + timezone.timedelta(days=number_of_bookings)

    result = LodgingRepository.get_list(
        date_from=date_from,
        date_to=date_to,
        number_of_people=number_of_people,
        number_of_rooms=number_of_rooms,
        city=city,
        available_only=available_only,
    )

    assert result.count() == number_of_lodgings - number_of_bookings

    # Get the reviewed lodging and assert for its average_rating
    reviewed_lodging = result.get(id=lodgings[number_of_bookings].id)
    assert reviewed_lodging.average_rating == average_reviews_rating

    # Assert that other (not reviewed) lodgings have no average_rating
    for lodging in result.exclude(id=lodgings[number_of_bookings].id):
        assert lodging.average_rating is None


@pytest.mark.django_db
def test_get_list_with_only_available_for_different_dates_succeeds():
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

    # Create reviews for one of the lodgings to get average_rating
    number_of_reviews = 4
    ReviewFactory.create_batch(size=number_of_reviews, lodging=lodgings[0])
    average_reviews_rating = Review.objects.aggregate(
        average_rating=Round(Avg("score"), precision=1)
    )["average_rating"]

    # Get list of all lodgings for a range completely different from the booked dates.
    date_from = timezone.now().date() + timezone.timedelta(days=30)
    date_to = date_from + timezone.timedelta(days=7)

    result = LodgingRepository.get_list(
        date_from=date_from,
        date_to=date_to,
        number_of_people=number_of_people,
        number_of_rooms=number_of_rooms,
        city=city,
        available_only=available_only,
    )

    assert result.count() == number_of_lodgings

    # Get the reviewed lodging and assert for its average_rating
    reviewed_lodging = result.get(id=lodgings[0].id)
    assert reviewed_lodging.average_rating == average_reviews_rating

    # Assert that other (not reviewed) lodgings have no average_rating
    for lodging in result.exclude(id=lodgings[0].id):
        assert lodging.average_rating is None
