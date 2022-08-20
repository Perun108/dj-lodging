from uuid import UUID

from django.core.exceptions import ValidationError

from djlodging.domain.lodgings.models import Country
from djlodging.domain.lodgings.models.city import City


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
