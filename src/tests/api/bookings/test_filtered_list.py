from datetime import datetime, timedelta

import pytest
from faker import Faker
from pytest_django.asserts import assertQuerysetEqual
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK

from djlodging.domain.bookings.models import Booking
from tests.domain.bookings.factories import BookingFactory
from tests.domain.lodgings.factories import LodgingFactory
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
        owner_1 = LodgingFactory()
        owner_2 = LodgingFactory()

        owner_1_bookings_number = 3
        owner_2_bookings_number = 2

        owner_1_bookings = BookingFactory.create_batch(
            size=owner_1_bookings_number, lodging=owner_1
        )
        owner_2_bookings = BookingFactory.create_batch(  # noqa
            size=owner_2_bookings_number, lodging=owner_2
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
            Booking.objects.filter(lodging=owner_1), owner_1_bookings, ordered=False
        )

    def test_list_filtered_by_kind(self, admin_api_client_pytest_fixture):
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
