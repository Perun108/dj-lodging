from typing import Dict, List, Optional, Union
from uuid import UUID

from django.db.models import QuerySet
from django.utils.timezone import now

from djlodging.api.pagination import paginate_queryset
from djlodging.domain.bookings.filters import BookingFilterSet
from djlodging.domain.bookings.models import Booking
from djlodging.domain.bookings.sorting import sort_queryset
from djlodging.domain.core.base_filters import Filter
from djlodging.domain.users.models import User


class BookingRepository:
    @classmethod
    def save(cls, booking: Booking) -> None:
        booking.save()

    @classmethod
    def get_all(cls) -> QuerySet[Booking]:
        return Booking.objects.all()

    @classmethod
    def get_list_by_user(cls, user: User) -> QuerySet[Booking]:
        return Booking.objects.filter(user=user)

    @classmethod
    def get_paginated_list_by_user(cls, user: User, query_params: dict) -> dict:
        bookings = cls.get_list_by_user(user)
        sorted_bookings = sort_queryset(bookings, query_params)
        return paginate_queryset(sorted_bookings, query_params)

    @classmethod
    def get_by_id(cls, booking_id: UUID) -> Booking:
        return Booking.objects.get(id=booking_id)

    @classmethod
    def get_by_reference_code(cls, reference_code: str) -> Optional[Booking]:
        return Booking.objects.filter(reference_code=reference_code).first()

    @classmethod
    def change_status(cls, booking: Booking, new_status: str) -> Booking:
        booking.status = new_status
        cls.save(booking)
        return booking

    @classmethod
    def get_filtered_list(cls, query_params: dict) -> Dict[str, Union[int, List[Booking]]]:
        qs = BookingRepository.get_all()
        filter_decorator = Filter(BookingFilterSet)
        filtered_qs = filter_decorator.filter(queryset=qs, query_params=query_params)
        sorted_qs = sort_queryset(filtered_qs, query_params)
        return paginate_queryset(sorted_qs, query_params)

    @classmethod
    def delete_by_id(cls, booking_id: UUID) -> tuple:
        booking = cls.get_by_id(booking_id)
        return booking.delete()

    @classmethod
    def delete_all_expired_unpaid_bookings(cls) -> None:
        expired_unpaid_bookings = Booking.objects.filter(
            status=Booking.Status.PAYMENT_PENDING, payment_expiration_time__lte=now()
        )
        expired_unpaid_bookings.delete()
