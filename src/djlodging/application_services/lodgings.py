from typing import Optional
from uuid import UUID

from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet

from djlodging.application_services.exceptions import (
    WrongBookingReferenceCode,
    WrongLodgingError,
    WrongOwnerError,
)
from djlodging.domain.bookings.repository import BookingRepository
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
    def create(cls, actor: User, country_id: UUID, name: str, region: str = "") -> City:
        # Check permissions to prevent unauthorized actions that circumvents API level permissions
        if not actor.is_staff:
            raise PermissionDenied
        country = CountryRepository.get_by_id(country_id)
        city = City(country=country, name=name, region=region)
        CityRepository.save(city)
        return city

    @classmethod
    def retrieve(cls, actor: User, city_id: UUID) -> City:
        # Check permissions to prevent unauthorized actions that circumvents API level permissions
        if not actor.is_staff:
            raise PermissionDenied
        city = CityRepository.get_by_id(city_id)
        return city

    @classmethod
    def update(cls, actor: User, city_id: UUID, **kwargs) -> City:
        # Check permissions to prevent unauthorized actions that circumvents API level permissions
        if not actor.is_staff:
            raise PermissionDenied
        city = CityRepository.get_by_id(city_id)
        for field, value in kwargs.items():
            setattr(city, field, value)
        CityRepository.save(city)
        return city

    @classmethod
    def get_list(cls, actor: User, country_id: UUID) -> QuerySet[City]:
        # Check permissions to prevent unauthorized actions that circumvents API level permissions
        if not actor.is_staff:
            raise PermissionDenied
        cities = CityRepository.get_list_by_country(country_id)
        return cities

    @classmethod
    def delete(cls, actor: User, city_id: UUID) -> tuple:
        # Check permissions to prevent unauthorized actions that circumvents API level permissions
        if not actor.is_staff:
            raise PermissionDenied
        return CityRepository.delete(city_id)


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

    @classmethod
    def update(cls, actor: User, lodging_id: UUID, **kwargs) -> Lodging:
        lodging = LodgingRepository.get_by_id(lodging_id)

        if lodging.owner != actor:
            raise WrongOwnerError

        for field, value in kwargs.items():
            setattr(lodging, field, value)
        LodgingRepository.save(lodging)
        return lodging

    @classmethod
    def delete(cls, actor: User, lodging_id: UUID) -> tuple:
        lodging = LodgingRepository.get_by_id(lodging_id)

        if lodging.owner != actor:
            raise WrongOwnerError

        return LodgingRepository.delete(lodging)


class ReviewService:
    @classmethod
    def create(
        cls, lodging_id: UUID, user: User, reference_code: str, text: str, score: int
    ) -> Review:
        lodging = LodgingRepository.get_by_id(lodging_id)

        booking = BookingRepository.get_by_reference_code(reference_code)
        if booking is None or booking.user != user:
            raise WrongBookingReferenceCode
        if booking.lodging != lodging:
            raise WrongLodgingError

        review = Review(lodging=lodging, user=user, text=text, score=score)
        ReviewRepository.save(review)
        return review

    @classmethod
    def update(cls, actor: User, review_id: UUID, **kwargs) -> Review:
        review = cls._verify_review_user_permissions(actor, review_id)
        for field, value in kwargs.items():
            setattr(review, field, value)
        ReviewRepository.save(review)
        return review

    @classmethod
    def delete(cls, actor: User, review_id: UUID) -> tuple:
        review = cls._verify_review_user_permissions(actor, review_id)
        return ReviewRepository.delete(review)

    @classmethod
    def _verify_review_user_permissions(cls, actor: User, review_id: UUID) -> Review:
        review = ReviewRepository.get_by_id(review_id=review_id)
        if review.user != actor:
            raise PermissionDenied
        return review

    @classmethod
    def retrieve_my(cls, actor: User, review_id: UUID) -> Review:
        return cls._verify_review_user_permissions(actor, review_id)
