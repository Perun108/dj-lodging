from django_filters import rest_framework as filters


class BookingFilterSet(filters.FilterSet):
    user_id = filters.UUIDFilter(field_name="user__id", lookup_expr="exact")
    date_from = filters.DateFilter(field_name="date_from", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="date_to", lookup_expr="lte")
    status = filters.CharFilter(field_name="status", lookup_expr="iexact")

    # lodging
    lodging_id = filters.UUIDFilter(field_name="lodging__id", lookup_expr="exact")
    owner_id = filters.UUIDFilter(field_name="lodging__owner__id", lookup_expr="exact")
    kind = filters.CharFilter(field_name="lodging__kind", lookup_expr="iexact")
    country_name = filters.CharFilter(
        field_name="lodging__city__country__name", lookup_expr="icontains"
    )
    region_name = filters.CharFilter(
        field_name="lodging__city__region__name", lookup_expr="icontains"
    )
    city_name = filters.CharFilter(field_name="lodging__city__name", lookup_expr="icontains")
    city_district = filters.CharFilter(field_name="lodging__district", lookup_expr="icontains")
    street = filters.CharFilter(field_name="lodging__street", lookup_expr="icontains")
    zip_code = filters.CharFilter(field_name="lodging__zip_code", lookup_expr="icontains")
    email = filters.CharFilter(field_name="lodging__email", lookup_expr="exact")
    number_of_people = filters.NumberFilter(
        field_name="lodging__number_of_people", lookup_expr="exact"
    )
    number_of_rooms = filters.NumberFilter(
        field_name="lodging__number_of_rooms", lookup_expr="exact"
    )
    price_gte = filters.NumberFilter(field_name="lodging__price", lookup_expr="gte")
    price_lte = filters.NumberFilter(field_name="lodging__price", lookup_expr="lte")
