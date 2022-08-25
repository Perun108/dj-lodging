from datetime import date
from typing import Optional
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db.models import Q, QuerySet

from djlodging.domain.lodgings.models import Country
from djlodging.domain.lodgings.models.city import City
from djlodging.domain.lodgings.models.lodging import Lodging


class CountryRepository:
    @classmethod
    def save(cls, country: Country) -> None:
        country.save()

    @classmethod
    def get_by_id(cls, country_id: UUID) -> None:
        try:
            return Country.objects.get(id=country_id)
        except Country.DoesNotExist:
            raise ValidationError("There is no country with this id")


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
    def get_available_at_destination_for_dates(
        cls,
        date_from: date,
        date_to: date,
        number_of_people: int,
        number_of_rooms: int,
        country: Optional[str] = "",
        city: Optional[str] = "",
        type: Optional[str] = "",
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

        if type:
            lodging_filter |= Q(type__exact=type)

        lodging_ids_list = Lodging.objects.filter(lodging_filter).values_list("id", flat=True)

        available = (
            Lodging.objects.filter(
                ~Q(booking__lodging__id__in=lodging_ids_list)
                | Q(id__in=lodging_ids_list) & Q(booking__date_to__lte=date_from)
                | Q(id__in=lodging_ids_list) & Q(booking__date_from__gte=date_to)
            )
            .distinct()
            .order_by(order)
        )

        return available
