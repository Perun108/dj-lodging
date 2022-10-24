from django.db.models import QuerySet

from djlodging.domain.bookings.filters import BookingFilterSet
from djlodging.domain.bookings.models import Booking
from djlodging.domain.bookings.repository import BookingRepository
from djlodging.domain.core.base_filters import Filter


class BookingService:
    @classmethod
    def get_filtered_list(cls, query_params) -> QuerySet[Booking]:
        qs = BookingRepository.get_all()
        filter_decorator = Filter(BookingFilterSet)
        return filter_decorator.filter(queryset=qs, query_params=query_params)
