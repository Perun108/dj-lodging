from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from faker import Faker
from pytest_django.asserts import assertQuerysetEqual
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK

from djlodging.domain.bookings.models import Booking
from djlodging.domain.lodgings.models.lodging import Lodging
from tests.domain.bookings.factories import BookingFactory
from tests.domain.lodgings.factories import CityFactory, CountryFactory, LodgingFactory
from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestQueryParamsFilteredList:
    def test_list_filtered_by_user_id(self, admin_api_client_pytest_fixture):
        user_1 = UserFactory()
        user_2 = UserFactory()

        user_1_bookings_number = 3
        user_2_bookings_number = 2

        user_1_bookings = BookingFactory.create_batch(size=user_1_bookings_number, user=user_1)
        user_2_bookings = BookingFactory.create_batch(  # noqa
            size=user_2_bookings_number, user=user_2
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"user_id": str(user_1.id)})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == user_1_bookings_number
        assert Booking.objects.count() == user_1_bookings_number + user_2_bookings_number

        bookings_ids_list = [item["id"] for item in response.data]
        user_1_bookings_ids_list = [str(item.id) for item in user_1_bookings]

        assert bookings_ids_list.sort() == user_1_bookings_ids_list.sort()
        assertQuerysetEqual(Booking.objects.filter(user=user_1), user_1_bookings, ordered=False)

    def test_list_filtered_by_current_date_from(self, admin_api_client_pytest_fixture):
        user_1 = UserFactory()
        user_2 = UserFactory()

        current_date_from = datetime.today().date()
        passed_date_from = current_date_from - timedelta(days=2)
        future_date_from = current_date_from + timedelta(days=2)

        # Create 1 passed booking to be filtered out.
        passed_booking = BookingFactory(user=user_1, date_from=passed_date_from)  # noqa

        # Create 4 booking for 2 users: 2 current and 2 future.
        bookings_list = []
        for user in [user_1, user_2]:
            for date in [current_date_from, future_date_from]:
                booking = BookingFactory(user=user, date_from=date)
                bookings_list.append(booking)

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"date_from": current_date_from})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == len(bookings_list)

        filtered_bookings_ids_list = [item["id"] for item in response.data]
        bookings_ids_list = [str(item.id) for item in bookings_list]

        assert len(filtered_bookings_ids_list) == len(bookings_ids_list)
        assert filtered_bookings_ids_list.sort() == bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(date_from__gte=current_date_from), bookings_list, ordered=False
        )

    def test_list_filtered_by_passed_date_from(self, admin_api_client_pytest_fixture):
        user_1 = UserFactory()
        user_2 = UserFactory()

        current_date_from = datetime.today().date()
        passed_date_from = current_date_from - timedelta(days=2)
        future_date_from = current_date_from + timedelta(days=2)

        # Create 1 passed booking.
        passed_booking = BookingFactory(user=user_1, date_from=passed_date_from)  # noqa

        # Create 4 booking for 2 users: 2 current and 2 future.
        bookings_list = []
        for user in [user_1, user_2]:
            for date in [current_date_from, future_date_from]:
                booking = BookingFactory(user=user, date_from=date)
                bookings_list.append(booking)

        bookings_list.append(passed_booking)

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"date_from": passed_date_from})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == len(bookings_list)

        filtered_bookings_ids_list = [item["id"] for item in response.data]
        bookings_ids_list = [str(item.id) for item in bookings_list]

        assert len(filtered_bookings_ids_list) == len(bookings_ids_list)
        assert filtered_bookings_ids_list.sort() == bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(date_from__gte=passed_date_from), bookings_list, ordered=False
        )

    def test_list_filtered_by_future_date_from(self, admin_api_client_pytest_fixture):
        user_1 = UserFactory()
        user_2 = UserFactory()

        current_date_from = datetime.today().date()
        passed_date_from = current_date_from - timedelta(days=2)
        future_date_from = current_date_from + timedelta(days=2)

        # Create 1 passed booking.
        passed_booking = BookingFactory(user=user_1, date_from=passed_date_from)  # noqa

        # Create 4 booking for 2 users: 2 current and 2 future.
        bookings_list = []
        for user in [user_1, user_2]:
            booking = BookingFactory(user=user, date_from=future_date_from)
            bookings_list.append(booking)

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"date_from": future_date_from})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == len(bookings_list)

        filtered_bookings_ids_list = [item["id"] for item in response.data]
        bookings_ids_list = [str(item.id) for item in bookings_list]

        assert len(filtered_bookings_ids_list) == len(bookings_ids_list)
        assert filtered_bookings_ids_list.sort() == bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(date_from__gte=future_date_from), bookings_list, ordered=False
        )

    def test_list_filtered_by_current_date_to(self, admin_api_client_pytest_fixture):
        user_1 = UserFactory()
        user_2 = UserFactory()

        current_date_to = datetime.today().date()
        passed_date_to = current_date_to - timedelta(days=2)
        future_date_to = current_date_to + timedelta(days=2)

        # Create 1 future booking to be filtered out
        future_booking = BookingFactory(user=user_1, date_to=future_date_to)  # noqa

        # Create 4 booking for 2 users: 2 current and 2 passed
        bookings_list = []
        for user in [user_1, user_2]:
            for date in [current_date_to, passed_date_to]:
                booking = BookingFactory(user=user, date_to=date)
                bookings_list.append(booking)

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"date_to": current_date_to})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == len(bookings_list)

        filtered_bookings_ids_list = [item["id"] for item in response.data]
        bookings_ids_list = [str(item.id) for item in bookings_list]

        assert len(filtered_bookings_ids_list) == len(bookings_ids_list)
        assert filtered_bookings_ids_list.sort() == bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(date_to__lte=current_date_to), bookings_list, ordered=False
        )

    def test_list_filtered_by_passed_date_to(self, admin_api_client_pytest_fixture):
        user_1 = UserFactory()
        user_2 = UserFactory()

        current_date_to = datetime.today().date()
        passed_date_to = current_date_to - timedelta(days=2)
        future_date_to = current_date_to + timedelta(days=2)

        # Create 1 future booking to be filtered out
        future_booking = BookingFactory(user=user_1, date_to=future_date_to)  # noqa

        # Create 1 current booking to be filtered out
        current_booking = BookingFactory(user=user_2, date_to=current_date_to)  # noqa

        # Create passed bookings for 2 users
        bookings_list = []
        for user in [user_1, user_2]:
            booking = BookingFactory(user=user, date_to=passed_date_to)
            bookings_list.append(booking)

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"date_to": passed_date_to})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == len(bookings_list)

        filtered_bookings_ids_list = [item["id"] for item in response.data]
        bookings_ids_list = [str(item.id) for item in bookings_list]

        assert len(filtered_bookings_ids_list) == len(bookings_ids_list)
        assert filtered_bookings_ids_list.sort() == bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(date_to__lte=passed_date_to), bookings_list, ordered=False
        )

    def test_list_filtered_by_future_date_to(self, admin_api_client_pytest_fixture):
        user_1 = UserFactory()
        user_2 = UserFactory()

        current_date_to = datetime.today().date()
        passed_date_to = current_date_to - timedelta(days=2)
        future_date_to = current_date_to + timedelta(days=2)

        # Create 1 passed booking
        passed_booking = BookingFactory(user=user_1, date_to=passed_date_to)  # noqa

        # Create 4 booking for 2 users: 2 current and 2 future
        bookings_list = []
        for user in [user_1, user_2]:
            booking = BookingFactory(user=user, date_to=future_date_to)
            bookings_list.append(booking)

        bookings_list.append(passed_booking)

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"date_to": future_date_to})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == len(bookings_list)

        filtered_bookings_ids_list = [item["id"] for item in response.data]
        bookings_ids_list = [str(item.id) for item in bookings_list]

        assert len(filtered_bookings_ids_list) == len(bookings_ids_list)
        assert filtered_bookings_ids_list.sort() == bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(date_to__lte=future_date_to), bookings_list, ordered=False
        )

    def test_list_filtered_by_status(self, admin_api_client_pytest_fixture):
        paid_bookings_number = 3
        payment_pending_bookings_number = 2

        paid_bookings = BookingFactory.create_batch(
            size=paid_bookings_number, status=Booking.Status.PAID
        )
        bookings_payment_pending = BookingFactory.create_batch(  # noqa
            size=payment_pending_bookings_number
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"status": Booking.Status.PAID})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == paid_bookings_number
        assert Booking.objects.count() == paid_bookings_number + payment_pending_bookings_number

        response_bookings_ids_list = [item["id"] for item in response.data]
        paid_bookings_ids_list = [str(item.id) for item in paid_bookings]

        assert response_bookings_ids_list.sort() == paid_bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(status=Booking.Status.PAID), paid_bookings, ordered=False
        )

    def test_list_filtered_by_lodging_id(self, admin_api_client_pytest_fixture):
        lodging_1 = LodgingFactory()
        lodging_2 = LodgingFactory()

        lodging_1_bookings_number = 3
        lodging_2_bookings_number = 2

        lodging_1_bookings = BookingFactory.create_batch(
            size=lodging_1_bookings_number, lodging=lodging_1
        )
        lodging_2_bookings = BookingFactory.create_batch(  # noqa
            size=lodging_2_bookings_number, lodging=lodging_2
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"lodging_id": str(lodging_1.id)})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == lodging_1_bookings_number
        assert Booking.objects.count() == lodging_1_bookings_number + lodging_2_bookings_number

        bookings_ids_list = [item["id"] for item in response.data]
        lodging_1_bookings_ids_list = [str(item.id) for item in lodging_1_bookings]

        assert bookings_ids_list.sort() == lodging_1_bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(lodging=lodging_1), lodging_1_bookings, ordered=False
        )

    def test_list_filtered_by_owner_id(self, admin_api_client_pytest_fixture):
        owner_1 = UserFactory()
        owner_2 = UserFactory()
        lodging_1 = LodgingFactory(owner=owner_1)
        lodging_2 = LodgingFactory(owner=owner_2)

        owner_1_bookings_number = 3
        owner_2_bookings_number = 2

        owner_1_bookings = BookingFactory.create_batch(
            size=owner_1_bookings_number, lodging=lodging_1
        )
        owner_2_bookings = BookingFactory.create_batch(  # noqa
            size=owner_2_bookings_number, lodging=lodging_2
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"owner_id": str(owner_1.id)})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == owner_1_bookings_number
        assert Booking.objects.count() == owner_1_bookings_number + owner_2_bookings_number

        bookings_ids_list = [item["id"] for item in response.data]
        owner_1_bookings_ids_list = [str(item.id) for item in owner_1_bookings]

        assert bookings_ids_list.sort() == owner_1_bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(lodging__owner=owner_1), owner_1_bookings, ordered=False
        )

    def test_list_filtered_by_kind(self, admin_api_client_pytest_fixture):
        hotel = LodgingFactory(kind=Lodging.Kind.HOTEL)
        apartment = LodgingFactory(kind=Lodging.Kind.APARTMENT)

        hotel_bookings_number = 3
        apartment_bookings_number = 2

        hotel_bookings = BookingFactory.create_batch(size=hotel_bookings_number, lodging=hotel)
        apartment_bookings = BookingFactory.create_batch(  # noqa
            size=apartment_bookings_number, lodging=apartment
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"kind": Lodging.Kind.HOTEL})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == hotel_bookings_number
        assert Booking.objects.count() == hotel_bookings_number + apartment_bookings_number

        response_bookings_ids_list = [item["id"] for item in response.data]
        hotel_bookings_ids_list = [str(item.id) for item in hotel_bookings]

        assert response_bookings_ids_list.sort() == hotel_bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(lodging__kind=Lodging.Kind.HOTEL),
            hotel_bookings,
            ordered=False,
        )

    def test_list_filtered_by_country_name(self, admin_api_client_pytest_fixture):
        country_1_lodging = LodgingFactory()
        country_2_lodging = LodgingFactory()

        country_1_bookings_number = 3
        country_2_bookings_number = 2

        country_1_bookings = BookingFactory.create_batch(
            size=country_1_bookings_number, lodging=country_1_lodging
        )
        country_2_bookings = BookingFactory.create_batch(  # noqa
            size=country_2_bookings_number, lodging=country_2_lodging
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(
            url, {"country_name": country_1_lodging.city.country.name}
        )

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == country_1_bookings_number
        assert Booking.objects.count() == country_1_bookings_number + country_2_bookings_number

        response_bookings_ids_list = [item["id"] for item in response.data]
        country_1_bookings_ids_list = [str(item.id) for item in country_1_bookings]

        assert response_bookings_ids_list.sort() == country_1_bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(
                lodging__city__country__name=country_1_lodging.city.country.name
            ),
            country_1_bookings,
            ordered=False,
        )

    # def test_list_filtered_by_country_name(self, admin_api_client_pytest_fixture):
    #     country_1 = CountryFactory()
    #     country_2 = CountryFactory()
    #     country_1_city = CityFactory(country=country_1)
    #     country_2_city = CityFactory(country=country_2)
    #     country_1_lodging = LodgingFactory(city=country_1_city)
    #     country_2_lodging = LodgingFactory(city=country_2_city)

    #     country_1_bookings_number = 3
    #     country_2_bookings_number = 2

    #     country_1_bookings = BookingFactory.create_batch(
    #         size=country_1_bookings_number, lodging=country_1_lodging
    #     )
    #     country_2_bookings = BookingFactory.create_batch(  # noqa
    #         size=country_2_bookings_number, lodging=country_2_lodging
    #     )

    #     url = reverse("bookings-list")
    #     response = admin_api_client_pytest_fixture.get(url, {"country_name": country_1.name})

    #     assert response.status_code == HTTP_200_OK
    #     assert len(response.data) == country_1_bookings_number
    #     assert Booking.objects.count() == country_1_bookings_number + country_2_bookings_number

    #     response_bookings_ids_list = [item["id"] for item in response.data]
    #     country_1_bookings_ids_list = [str(item.id) for item in country_1_bookings]

    #     assert response_bookings_ids_list.sort() == country_1_bookings_ids_list.sort()
    #     assertQuerysetEqual(
    #         Booking.objects.filter(lodging__city__country__name=country_1.name),
    #         country_1_bookings,
    #         ordered=False,
    #     )

    def test_list_filtered_by_country_region(self, admin_api_client_pytest_fixture):
        country = CountryFactory()
        region_1 = fake.name()
        region_2 = fake.name()
        city_1 = CityFactory(country=country, region=region_1)
        city_2 = CityFactory(country=country, region=region_2)
        region_1_lodging = LodgingFactory(city=city_1)
        region_2_lodging = LodgingFactory(city=city_2)

        region_1_bookings_number = 3
        region_2_bookings_number = 2

        region_1_bookings = BookingFactory.create_batch(
            size=region_1_bookings_number, lodging=region_1_lodging
        )
        region_2_bookings = BookingFactory.create_batch(  # noqa
            size=region_2_bookings_number, lodging=region_2_lodging
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"country_region": region_1})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == region_1_bookings_number
        assert Booking.objects.count() == region_1_bookings_number + region_2_bookings_number

        response_bookings_ids_list = [item["id"] for item in response.data]
        region_1_bookings_ids_list = [str(item.id) for item in region_1_bookings]

        assert response_bookings_ids_list.sort() == region_1_bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(lodging__city__region=region_1),
            region_1_bookings,
            ordered=False,
        )

    def test_list_filtered_by_city_name(self, admin_api_client_pytest_fixture):
        city_1 = CityFactory()
        city_2 = CityFactory()
        city_1_lodging = LodgingFactory(city=city_1)
        city_2_lodging = LodgingFactory(city=city_2)

        city_1_bookings_number = 3
        city_2_bookings_number = 2

        city_1_bookings = BookingFactory.create_batch(
            size=city_1_bookings_number, lodging=city_1_lodging
        )
        city_2_bookings = BookingFactory.create_batch(  # noqa
            size=city_2_bookings_number, lodging=city_2_lodging
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"city_name": city_1.name})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == city_1_bookings_number
        assert Booking.objects.count() == city_1_bookings_number + city_2_bookings_number

        response_bookings_ids_list = [item["id"] for item in response.data]
        city_1_bookings_ids_list = [str(item.id) for item in city_1_bookings]

        assert response_bookings_ids_list.sort() == city_1_bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(lodging__city__name=city_1.name),
            city_1_bookings,
            ordered=False,
        )

    def test_list_filtered_by_city_district(self, admin_api_client_pytest_fixture):
        district_1 = fake.name()
        district_2 = fake.name()
        district_1_lodging = LodgingFactory(district=district_1)
        district_2_lodging = LodgingFactory(district=district_2)

        district_1_lodging_bookings_number = 3
        district_2_lodging_bookings_number = 2

        district_1_bookings = BookingFactory.create_batch(
            size=district_1_lodging_bookings_number, lodging=district_1_lodging
        )
        district_2_bookings = BookingFactory.create_batch(  # noqa
            size=district_2_lodging_bookings_number, lodging=district_2_lodging
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"city_district": district_1})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == district_1_lodging_bookings_number
        assert (
            Booking.objects.count()
            == district_1_lodging_bookings_number + district_2_lodging_bookings_number
        )

        response_bookings_ids_list = [item["id"] for item in response.data]
        district_1_bookings_ids_list = [str(item.id) for item in district_1_bookings]

        assert response_bookings_ids_list.sort() == district_1_bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(lodging__district=district_1),
            district_1_bookings,
            ordered=False,
        )

    def test_list_filtered_by_street(self, admin_api_client_pytest_fixture):
        street_1 = fake.name()
        street_2 = fake.name()
        street_1_lodging = LodgingFactory(street=street_1)
        street_2_lodging = LodgingFactory(street=street_2)

        street_1_lodging_bookings_number = 3
        street_2_lodging_bookings_number = 2

        street_1_bookings = BookingFactory.create_batch(
            size=street_1_lodging_bookings_number, lodging=street_1_lodging
        )
        street_2_bookings = BookingFactory.create_batch(  # noqa
            size=street_2_lodging_bookings_number, lodging=street_2_lodging
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"street": street_1})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == street_1_lodging_bookings_number
        assert (
            Booking.objects.count()
            == street_1_lodging_bookings_number + street_2_lodging_bookings_number
        )

        response_bookings_ids_list = [item["id"] for item in response.data]
        street_1_bookings_ids_list = [str(item.id) for item in street_1_bookings]

        assert response_bookings_ids_list.sort() == street_1_bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(lodging__street=street_1),
            street_1_bookings,
            ordered=False,
        )

    def test_list_filtered_by_zip_code(self, admin_api_client_pytest_fixture):
        zip_code_1 = fake.postcode()
        zip_code_2 = fake.postcode()
        zip_code_1_lodging = LodgingFactory(zip_code=zip_code_1)
        zip_code_2_lodging = LodgingFactory(zip_code=zip_code_2)

        zip_code_1_lodging_bookings_number = 3
        zip_code_2_lodging_bookings_number = 2

        zip_code_1_bookings = BookingFactory.create_batch(
            size=zip_code_1_lodging_bookings_number, lodging=zip_code_1_lodging
        )
        zip_code_2_bookings = BookingFactory.create_batch(  # noqa
            size=zip_code_2_lodging_bookings_number, lodging=zip_code_2_lodging
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"zip_code": zip_code_1})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == zip_code_1_lodging_bookings_number
        assert (
            Booking.objects.count()
            == zip_code_1_lodging_bookings_number + zip_code_2_lodging_bookings_number
        )

        response_bookings_ids_list = [item["id"] for item in response.data]
        zip_code_1_bookings_ids_list = [str(item.id) for item in zip_code_1_bookings]

        assert response_bookings_ids_list.sort() == zip_code_1_bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(lodging__zip_code=zip_code_1),
            zip_code_1_bookings,
            ordered=False,
        )

    def test_list_filtered_by_email(self, admin_api_client_pytest_fixture):
        email_1 = fake.email()
        email_2 = fake.email()
        email_1_lodging = LodgingFactory(email=email_1)
        email_2_lodging = LodgingFactory(email=email_2)

        email_1_lodging_bookings_number = 3
        email_2_lodging_bookings_number = 2

        email_1_bookings = BookingFactory.create_batch(
            size=email_1_lodging_bookings_number, lodging=email_1_lodging
        )
        email_2_bookings = BookingFactory.create_batch(  # noqa
            size=email_2_lodging_bookings_number, lodging=email_2_lodging
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"email": email_1})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == email_1_lodging_bookings_number
        assert (
            Booking.objects.count()
            == email_1_lodging_bookings_number + email_2_lodging_bookings_number
        )

        response_bookings_ids_list = [item["id"] for item in response.data]
        email_1_bookings_ids_list = [str(item.id) for item in email_1_bookings]

        assert response_bookings_ids_list.sort() == email_1_bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(lodging__email=email_1),
            email_1_bookings,
            ordered=False,
        )

    def test_list_filtered_by_number_of_people(self, admin_api_client_pytest_fixture):
        number_of_people_1 = 2
        number_of_people_2 = 3
        lodging_1 = LodgingFactory(number_of_people=number_of_people_1)
        lodging_2 = LodgingFactory(number_of_people=number_of_people_2)

        lodging_1_bookings_number = 3
        lodging_2_bookings_number = 2

        lodging_1_bookings = BookingFactory.create_batch(
            size=lodging_1_bookings_number, lodging=lodging_1
        )
        lodging_2_bookings = BookingFactory.create_batch(  # noqa
            size=lodging_2_bookings_number, lodging=lodging_2
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(
            url, {"number_of_people": number_of_people_1}
        )

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == lodging_1_bookings_number
        assert Booking.objects.count() == lodging_1_bookings_number + lodging_2_bookings_number

        response_bookings_ids_list = [item["id"] for item in response.data]
        lodging_1_bookings_ids_list = [str(item.id) for item in lodging_1_bookings]

        assert response_bookings_ids_list.sort() == lodging_1_bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(lodging__number_of_people=number_of_people_1),
            lodging_1_bookings,
            ordered=False,
        )

    def test_list_filtered_by_number_of_rooms(self, admin_api_client_pytest_fixture):
        number_of_rooms_1 = 2
        number_of_rooms_2 = 3
        lodging_1 = LodgingFactory(number_of_rooms=number_of_rooms_1)
        lodging_2 = LodgingFactory(number_of_rooms=number_of_rooms_2)

        lodging_1_bookings_number = 3
        lodging_2_bookings_number = 2

        lodging_1_bookings = BookingFactory.create_batch(
            size=lodging_1_bookings_number, lodging=lodging_1
        )
        lodging_2_bookings = BookingFactory.create_batch(  # noqa
            size=lodging_2_bookings_number, lodging=lodging_2
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"number_of_rooms": number_of_rooms_1})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == lodging_1_bookings_number
        assert Booking.objects.count() == lodging_1_bookings_number + lodging_2_bookings_number

        response_bookings_ids_list = [item["id"] for item in response.data]
        lodging_1_bookings_ids_list = [str(item.id) for item in lodging_1_bookings]

        assert response_bookings_ids_list.sort() == lodging_1_bookings_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(lodging__number_of_rooms=number_of_rooms_1),
            lodging_1_bookings,
            ordered=False,
        )

    def test_list_filtered_by_price_gte(self, admin_api_client_pytest_fixture):
        low_price = Decimal("9.99")
        medium_price = Decimal("50.01")
        high_price = Decimal("99.99")

        low_price_lodging = LodgingFactory(price=low_price)
        medium_price_lodging = LodgingFactory(price=medium_price)
        high_price_lodging = LodgingFactory(price=high_price)

        low_price_bookings_number = 3
        medium_price_bookings_number = 2
        high_price_bookings_number = 1

        low_price_bookings = BookingFactory.create_batch(  # noqa
            size=low_price_bookings_number, lodging=low_price_lodging
        )
        medium_price_bookings = BookingFactory.create_batch(
            size=medium_price_bookings_number, lodging=medium_price_lodging
        )
        high_price_bookings = BookingFactory.create_batch(  # noqa
            size=high_price_bookings_number, lodging=high_price_lodging
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"price_gte": medium_price})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == medium_price_bookings_number + high_price_bookings_number
        assert (
            Booking.objects.count()
            == low_price_bookings_number
            + medium_price_bookings_number
            + high_price_bookings_number
        )

        response_bookings_ids_list = [item["id"] for item in response.data]
        result_bookings = medium_price_bookings + high_price_bookings
        result_booking_ids_list = [str(item.id) for item in result_bookings]

        assert response_bookings_ids_list.sort() == result_booking_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(lodging__price__gte=medium_price),
            result_bookings,
            ordered=False,
        )

    def test_list_filtered_by_price_lte(self, admin_api_client_pytest_fixture):
        low_price = Decimal("9.99")
        medium_price = Decimal("50.01")
        high_price = Decimal("99.99")

        low_price_lodging = LodgingFactory(price=low_price)
        medium_price_lodging = LodgingFactory(price=medium_price)
        high_price_lodging = LodgingFactory(price=high_price)

        low_price_bookings_number = 3
        medium_price_bookings_number = 2
        high_price_bookings_number = 1

        low_price_bookings = BookingFactory.create_batch(
            size=low_price_bookings_number, lodging=low_price_lodging
        )
        medium_price_bookings = BookingFactory.create_batch(
            size=medium_price_bookings_number, lodging=medium_price_lodging
        )
        high_price_bookings = BookingFactory.create_batch(  # noqa
            size=high_price_bookings_number, lodging=high_price_lodging
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(url, {"price_lte": medium_price})

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == low_price_bookings_number + medium_price_bookings_number
        assert (
            Booking.objects.count()
            == low_price_bookings_number
            + medium_price_bookings_number
            + high_price_bookings_number
        )

        response_bookings_ids_list = [item["id"] for item in response.data]
        result_bookings = low_price_bookings + medium_price_bookings
        result_booking_ids_list = [str(item.id) for item in result_bookings]

        assert response_bookings_ids_list.sort() == result_booking_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(lodging__price__lte=medium_price),
            result_bookings,
            ordered=False,
        )

    def test_list_filtered_by_both_price_lte_and_price_gte(self, admin_api_client_pytest_fixture):
        low_price = Decimal("9.99")
        medium_price = Decimal("50.01")
        high_price = Decimal("99.99")
        highest_price = Decimal("999.99")

        low_price_lodging = LodgingFactory(price=low_price)
        medium_price_lodging = LodgingFactory(price=medium_price)
        high_price_lodging = LodgingFactory(price=high_price)
        highest_price_lodging = LodgingFactory(price=highest_price)

        low_price_bookings_number = 3
        medium_price_bookings_number = 2
        high_price_bookings_number = 1
        highest_price_bookings_number = 2

        low_price_bookings = BookingFactory.create_batch(  # noqa
            size=low_price_bookings_number, lodging=low_price_lodging
        )
        medium_price_bookings = BookingFactory.create_batch(
            size=medium_price_bookings_number, lodging=medium_price_lodging
        )
        high_price_bookings = BookingFactory.create_batch(
            size=high_price_bookings_number, lodging=high_price_lodging
        )
        highest_price_bookings = BookingFactory.create_batch(  # noqa
            size=highest_price_bookings_number, lodging=highest_price_lodging
        )

        url = reverse("bookings-list")
        response = admin_api_client_pytest_fixture.get(
            url, {"price_lte": high_price, "price_gte": medium_price}
        )

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == medium_price_bookings_number + high_price_bookings_number
        assert (
            Booking.objects.count()
            == low_price_bookings_number
            + medium_price_bookings_number
            + high_price_bookings_number
            + highest_price_bookings_number
        )

        response_bookings_ids_list = [item["id"] for item in response.data]
        result_bookings = medium_price_bookings + high_price_bookings
        result_booking_ids_list = [str(item.id) for item in result_bookings]

        assert response_bookings_ids_list.sort() == result_booking_ids_list.sort()
        assertQuerysetEqual(
            Booking.objects.filter(
                lodging__price__lte=high_price, lodging__price__gte=medium_price
            ),
            result_bookings,
            ordered=False,
        )
