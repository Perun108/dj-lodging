from datetime import date
from typing import Dict, List, Optional, Union
from uuid import UUID

from django.db.models import Avg, Case, Q, QuerySet, Value, When
from django.db.models.functions import Round

from djlodging.api.pagination import paginate_queryset
from djlodging.domain.bookings.sorting import sort_queryset
from djlodging.domain.core.base_exceptions import DjLodgingValidationError
from djlodging.domain.lodgings.models import Country
from djlodging.domain.lodgings.models.city import City
from djlodging.domain.lodgings.models.lodging import Lodging
from djlodging.domain.lodgings.models.review import Review
from djlodging.domain.users.models import User


class CountryRepository:
    @classmethod
    def save(cls, country: Country) -> None:
        country.save()

    @classmethod
    def get_by_id(cls, country_id: UUID) -> Country:
        return Country.objects.get(id=country_id)

    @classmethod
    def get_all(cls) -> QuerySet[Country]:
        return Country.objects.all()

    @classmethod
    def delete(cls, country_id: UUID) -> tuple:
        country = cls.get_by_id(country_id)
        return country.delete()

    @classmethod
    def get_list(cls, query_params: dict) -> Dict[str, Union[int, List[Country]]]:
        countries = cls.get_all()
        sorted_countries = sort_queryset(countries, query_params)
        return paginate_queryset(sorted_countries, query_params)


class CityRepository:
    @classmethod
    def save(cls, city: City) -> None:
        city.save()

    @classmethod
    def get_by_id(cls, city_id: UUID) -> City:
        return City.objects.get(id=city_id)

    @classmethod
    def get_list_by_country(cls, country_id: UUID) -> QuerySet[City]:
        return City.objects.filter(country__id=country_id)

    @classmethod
    def get_paginated_list_by_country(
        cls, country_id: UUID, query_params: dict
    ) -> Dict[str, Union[int, List[City]]]:
        cities = cls.get_list_by_country(country_id)
        sorted_cities = sort_queryset(cities, query_params)
        return paginate_queryset(sorted_cities, query_params)

    @classmethod
    def delete(cls, city_id: UUID) -> tuple:
        city = cls.get_by_id(city_id)
        return city.delete()


class LodgingRepository:
    @classmethod
    def get_by_id(cls, lodging_id: UUID) -> Lodging:
        return Lodging.objects.get(id=lodging_id)

    @classmethod
    def save(cls, lodging: Lodging) -> None:
        lodging.save()

    @classmethod
    def delete(cls, lodging: Lodging) -> tuple:
        return lodging.delete()

    @classmethod
    def get_filtered_list(cls, query_params: dict) -> QuerySet[Lodging]:
        date_from = query_params.get("date_from")
        date_to = query_params.get("date_to")
        number_of_people = int(query_params.get("number_of_people", 1))
        number_of_rooms = int(query_params.get("number_of_rooms", 1))
        kind = query_params.get("kind", "")
        available_only = bool(query_params.get("available_only", False))
        country = query_params.get("country")
        city = query_params.get("city")

        if not (country or city):
            raise DjLodgingValidationError("You must provide either a city or a country!")

        lodging_filter = cls._construct_lodging_filter(
            number_of_people, number_of_rooms, kind, country, city
        )
        query_expression = cls._generate_query_expression_for_filter(
            date_from, date_to, lodging_filter
        )
        filtered_lodgings = cls._get_filtered_lodgings(available_only, query_expression)
        # Add average_rating to each lodging
        result = cls._annotate_lodgings_with_average_ratings(filtered_lodgings).distinct()
        return result

    @classmethod
    def _generate_query_expression_for_filter(
        cls, date_from: date, date_to: date, lodging_filter: Q
    ) -> Q:
        filtered_lodgings = Lodging.objects.filter(lodging_filter)
        filtered_lodgings_ids_list = filtered_lodgings.values_list("id", flat=True)
        query_expression = (
            ~Q(booking__lodging__id__in=filtered_lodgings_ids_list)
            | Q(id__in=filtered_lodgings_ids_list) & Q(booking__date_to__lte=date_from)
            | Q(id__in=filtered_lodgings_ids_list) & Q(booking__date_from__gte=date_to)
        )
        return query_expression

    @classmethod
    def _get_filtered_lodgings(
        cls, available_only: bool, query_expression: Q
    ) -> QuerySet[Lodging]:
        if available_only:
            # TODO: Filter for Bookings status!
            filtered_lodgings = Lodging.objects.filter(query_expression)
        else:
            filtered_lodgings = Lodging.objects.annotate(
                available=Case(
                    When(
                        query_expression,
                        then=Value(True),
                    ),
                    default=Value(False),
                )
            )

        return filtered_lodgings

    @classmethod
    def _construct_lodging_filter(
        cls,
        number_of_people: int,
        number_of_rooms: int,
        kind: str,
        country: Optional[str],
        city: Optional[str],
    ) -> Q:
        lodging_filter = Q(
            number_of_people__gte=number_of_people,
            number_of_rooms__exact=number_of_rooms,
        )

        if city and country:
            lodging_filter |= Q(city__name__exact=city, city__country__name__exact=country)
        elif country:
            lodging_filter |= Q(city__country__name__exact=country)
        else:
            raise DjLodgingValidationError(
                "You must provide a city name with a country name! "
                "Or at least the name of the country."
            )

        if kind:
            lodging_filter |= Q(kind__exact=kind)
        return lodging_filter

    @classmethod
    def _annotate_lodgings_with_average_ratings(
        cls, filtered_lodgings: QuerySet
    ) -> QuerySet[Lodging]:
        return filtered_lodgings.annotate(average_rating=Round(Avg("reviews__score"), precision=1))

    @classmethod
    def get_paginated_filtered_list(
        cls, query_params: dict
    ) -> Dict[str, Union[int, List[Lodging]]]:
        lodgings = cls.get_filtered_list(query_params)
        sorted_lodgings = sort_queryset(lodgings, query_params)
        return paginate_queryset(sorted_lodgings, query_params)

    @classmethod
    def retrieve_lodging_with_average_rating(cls, lodging_id: UUID) -> Optional[Lodging]:
        lodging = Lodging.objects.filter(id=lodging_id)
        return cls._annotate_lodgings_with_average_ratings(lodging).first()


class ReviewRepository:
    @classmethod
    def save(cls, review: Review) -> None:
        review.save()

    @classmethod
    def get_by_id(cls, review_id: UUID) -> Review:
        return Review.objects.get(id=review_id)

    @classmethod
    def get_list_by_lodging(cls, lodging_id: UUID) -> QuerySet[Review]:
        return Review.objects.filter(lodging__id=lodging_id)

    @classmethod
    def get_paginated_list_by_lodging(
        cls, lodging_id: UUID, query_params: dict
    ) -> Dict[str, Union[int, List[Review]]]:
        reviews = cls.get_list_by_lodging(lodging_id)
        sorted_reviews = sort_queryset(reviews, query_params)
        return paginate_queryset(sorted_reviews, query_params)

    @classmethod
    def delete(cls, review: Review) -> tuple:
        return review.delete()

    @classmethod
    def get_list_by_user(cls, user: User) -> QuerySet[Review]:
        return Review.objects.filter(user=user)

    @classmethod
    def get_paginated_list_by_user(
        cls, user: User, query_params: dict
    ) -> Dict[str, Union[int, List[Review]]]:
        my_reviews = cls.get_list_by_user(user)
        my_sorted_reviews = sort_queryset(my_reviews, query_params)
        return paginate_queryset(my_sorted_reviews, query_params)
