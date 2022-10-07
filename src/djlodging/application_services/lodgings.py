from typing import Optional
from uuid import UUID

from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet

from djlodging.domain.lodgings.models import City, Country
from djlodging.domain.lodgings.models.lodging import Lodging
from djlodging.domain.lodgings.models.review import Review
from djlodging.domain.lodgings.repositories import (
    CityRepository,
    CountryRepository,
    LodgingRepository,
    ReviewRepository,
)
from djlodging.domain.users.models import User


class CountryService:
    @classmethod
    def create(cls, *, actor, name: str) -> Country:
        # Check permissions to prevent unauthorized actions that circumvents API level permissions
        if not actor.is_staff:
            raise PermissionDenied
        country = Country(name=name)
        CountryRepository.save(country)
        return country

    @classmethod
    def retrieve(cls, *, actor, country_id: UUID) -> Country:
        # Check permissions to prevent unauthorized actions that circumvents API level permissions
        if not actor.is_staff:
            raise PermissionDenied
        return CountryRepository.get_by_id(country_id=country_id)

    @classmethod
    def get_list(cls, *, actor) -> QuerySet[Country]:
        # Check permissions to prevent unauthorized actions that circumvents API level permissions
        if not actor.is_staff:
            raise PermissionDenied
        return CountryRepository.get_all()

    @classmethod
    def update(cls, *, actor, country_id: UUID, **kwargs) -> Country:
        # Check permissions to prevent unauthorized actions that circumvents API level permissions
        if not actor.is_staff:
            raise PermissionDenied

        country = CountryRepository.get_by_id(country_id=country_id)
        for field, value in kwargs.items():
            setattr(country, field, value)
        CountryRepository.save(country)
        return country

    @classmethod
    def delete(cls, *, actor, country_id: UUID) -> tuple:
        # Check permissions to prevent unauthorized actions that circumvents API level permissions
        if not actor.is_staff:
            raise PermissionDenied
        return CountryRepository.delete(country_id)


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


class LodgingService:
    @classmethod
    def create(
        cls,
        actor: User,
        name: str,
        kind: str,
        city_id: UUID,
        street: str,
        house_number: str,
        zip_code: str,
        price: int,
        email: Optional[str] = "",
        phone_number: Optional[str] = "",
        district: Optional[str] = "",
    ) -> Lodging:

        # Check permissions to prevent unauthorized actions that circumvents API level permissions
        if not actor.is_partner:
            raise PermissionDenied

        city = CityRepository.get_by_id(city_id)

        lodging = Lodging(
            name=name,
            kind=kind,
            owner=actor,
            city=city,
            district=district,
            street=street,
            house_number=house_number,
            zip_code=zip_code,
            phone_number=phone_number,
            email=email,
            price=price,
        )
        LodgingRepository.save(lodging)
        return lodging


class ReviewService:
    @classmethod
    def create(cls, lodging_id: UUID, user: User, text: str, score: int) -> Review:
        lodging = LodgingRepository.get_by_id(lodging_id)
        review = Review(lodging=lodging, user=user, text=text, score=score)
        ReviewRepository.save(review)
        return review
