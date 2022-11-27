from uuid import UUID

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.timezone import now, timedelta

from djlodging.domain.users.models import User


class UserRepository:
    @classmethod
    def save(cls, user):
        user.save()

    @classmethod
    def get_by_id(cls, user_id) -> User:
        return User.objects.get(id=user_id)

    @classmethod
    def get_user_by_security_token(cls, security_token: UUID) -> User:
        return User.objects.get(security_token=security_token)

    @classmethod
    def get_user_by_security_token_and_email(cls, security_token, email) -> User:
        user = User.objects.filter(security_token=security_token, email=email).first()
        if user is None:
            raise ValidationError("Such user does not exist")
        return user

    @classmethod
    def get_user_by_id_and_security_token(cls, user_id: UUID, security_token: UUID) -> User:
        user = User.objects.filter(id=user_id, security_token=security_token).first()
        if user is None:
            raise ValidationError(
                "User does not exist or have been deleted after sign up time had passed."
            )
        return user

    @classmethod
    def update(cls, user: User, **kwargs) -> User:
        for field, value in kwargs.items():
            setattr(user, field, value)
        cls.save(user)
        return user

    @classmethod
    def get_by_email(cls, email: str) -> User:
        return User.objects.get(email=email)

    @classmethod
    def delete_by_id(cls, user_id: UUID) -> tuple:
        user = cls.get_by_id(user_id)
        return user.delete()

    @classmethod
    def delete_users_with_unfinished_registration(cls) -> None:
        unregistered_users = User.objects.filter(
            is_active=False,
            security_token_expiration_time__lte=now()
            - timedelta(hours=settings.SECURITY_TOKEN_LIFE_TIME_IN_HOURS),
        )
        unregistered_users.delete()


class PaymentProviderUserRepository:
    @classmethod
    def save(cls, payment_provider_user):
        payment_provider_user.save()
