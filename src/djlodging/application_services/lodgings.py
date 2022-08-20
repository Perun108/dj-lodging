from django.core.exceptions import PermissionDenied

from djlodging.domain.lodgings.models import City, Country
from djlodging.domain.lodgings.repositories import CityRepository, CountryRepository
from djlodging.domain.users.models import User

# from djlodging.domain.lodgings.models.lodging import Lodging


class CountryService:
    @classmethod
    def create(cls, *, actor, name: str) -> Country:
        # Check permissions to prevent unauthorized actions that circumvents API level permissions
        if not actor.is_staff:
            raise PermissionDenied
        country = Country(name=name)
        CountryRepository.save(country)
        return country


class CityService:
    @classmethod
    def create(cls, actor: User, country_id, name: str, region: str = "") -> City:
        # Check permissions to prevent unauthorized actions that circumvents API level permissions
        if not actor.is_staff:
            raise PermissionDenied
        country = CountryRepository.get_by_id(country_id)
        city = City(country=country, name=name, region=region)
        CityRepository.save(city)
        return city


# class LodgingService:
#     @classmethod
#     def create(
#         cls,
#         name: str,
#         type: str,
#         city_id: UUID,
#         district: str,
#         street: str,
#         house_number: str,
#         zip_code: str,
#         phone_number: str,
#         email: str,
#         image_id: Optional[str] = None,
#     ) -> Lodging:
#         pass
#         lodging = Lodging(
#             name = name
#             type = type
#             city =
#             district = (optional)
#             street =
#             house_number =
#             zip_code =
#             phone_number =
#             email =
#             image = )
