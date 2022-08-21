from uuid import UUID

from django.core.exceptions import ValidationError

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
