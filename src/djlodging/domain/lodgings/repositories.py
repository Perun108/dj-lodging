from datetime import date
from typing import Optional
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db.models import Avg, Case, Q, QuerySet, Value, When
from django.db.models.functions import Round

from djlodging.domain.lodgings.models import Country
from djlodging.domain.lodgings.models.city import City
from djlodging.domain.lodgings.models.lodging import Lodging
from djlodging.domain.lodgings.models.review import Review


class CountryRepository:
    @classmethod
    def save(cls, country: Country) -> None:
        country.save()

    @classmethod
    def get_by_id(cls, country_id: UUID) -> Country:
        try:
            return Country.objects.get(id=country_id)
        except Country.DoesNotExist:
            raise ValidationError("There is no country with this id")

    @classmethod
    def get_all(cls) -> QuerySet[Country]:
        return Country.objects.all()

    @classmethod
    def delete(cls, country_id: UUID) -> tuple:
        country = cls.get_by_id(country_id)
        return country.delete()


class CityRepository:
    @classmethod
    def save(cls, city: City) -> None:
        city.save()

    @classmethod
    def get_by_id(cls, city_id: UUID) -> City:
        try:
            return City.objects.get(id=city_id)
        except City.DoesNotExist:
            raise ValidationError("There is no city with this id")

    @classmethod
    def get_list_by_country(cls, country_id: UUID) -> QuerySet[City]:
        return City.objects.filter(country__id=country_id)

    @classmethod
    def delete(cls, city_id: UUID) -> tuple:
        city = cls.get_by_id(city_id)
        return city.delete()


class LodgingRepository:
    @classmethod
    def get_by_id(cls, lodging_id: UUID) -> Lodging:
        try:
            return Lodging.objects.get(id=lodging_id)
        except Lodging.DoesNotExist:
            raise ValidationError("There is no lodging with this id")

    @classmethod
    def save(cls, lodging: Lodging) -> None:
        lodging.save()

    @classmethod
    def get_list(
        cls,
        date_from: date,
        date_to: date,
        number_of_people: int,
        number_of_rooms: int,
        country: Optional[str] = "",
        city: Optional[str] = "",
        kind: Optional[str] = "",
        available_only: bool = False,
        order: Optional[str] = "-price",
    ) -> QuerySet:

        lodging_filter = Q(
            number_of_people__gte=number_of_people,
            number_of_rooms__exact=number_of_rooms,
        )

        if city:
            lodging_filter |= Q(city__name__exact=city)
        elif country:
            lodging_filter |= Q(country__name__exact=country)
        else:
            raise ValidationError("You must specify either city or country")

        if kind:
            lodging_filter |= Q(kind__exact=kind)

        filtered_lodgings = Lodging.objects.filter(lodging_filter)
        filtered_lodgings_ids_list = filtered_lodgings.values_list("id", flat=True)

        query_expression = (
            ~Q(booking__lodging__id__in=filtered_lodgings_ids_list)
            | Q(id__in=filtered_lodgings_ids_list) & Q(booking__date_to__lte=date_from)
            | Q(id__in=filtered_lodgings_ids_list) & Q(booking__date_from__gte=date_to)
        )

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
        # Add average_rating to each lodging
        result = cls._annotate_lodgings_with_average_ratings(filtered_lodgings)
        return result.distinct().order_by(order)

    @classmethod
    def _annotate_lodgings_with_average_ratings(cls, filtered_lodgings: QuerySet):
        return filtered_lodgings.annotate(average_rating=Round(Avg("reviews__score"), precision=1))

    @classmethod
    def retrieve_lodging_with_average_rating(cls, lodging_id: UUID):
        lodging = Lodging.objects.filter(id=lodging_id)
        return cls._annotate_lodgings_with_average_ratings(lodging).first()


class ReviewRepository:
    @classmethod
    def save(cls, review: Review) -> None:
        review.save()

    @classmethod
    def get_list(cls, lodging_id: UUID) -> QuerySet:
        return Review.objects.filter(lodging__id=lodging_id)
