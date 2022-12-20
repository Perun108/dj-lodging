from uuid import UUID

from django.contrib.auth import get_user_model
from django.utils.timezone import now

from djlodging.domain.users.constants import (
    USER_DOES_NOT_EXIST_MESSAGE,
    USER_DOES_NOT_EXIST_OR_WAS_DELETED_MESSAGE,
)
from djlodging.domain.users.exceptions import UserDoesNotExist
from djlodging.domain.users.models import PaymentProviderUser
from djlodging.domain.users.models import User as UserModel

User = get_user_model()


class UserRepository:
    @classmethod
    def save(cls, user: UserModel) -> None:
        user.save()

    @classmethod
    def get_by_id(cls, user_id: UUID) -> UserModel:
        return User.objects.get(id=user_id)

    @classmethod
    def get_user_by_security_token(cls, security_token: UUID) -> UserModel:
        return User.objects.get(security_token=security_token)

    @classmethod
    def get_user_by_security_token_and_email(cls, security_token, email) -> UserModel:
        user = User.objects.filter(security_token=security_token, email=email).first()
        if user is None:
            raise UserDoesNotExist(message=USER_DOES_NOT_EXIST_MESSAGE)
        return user

    @classmethod
    def get_user_by_id_and_security_token(cls, user_id: UUID, security_token: UUID) -> UserModel:
        user = User.objects.filter(id=user_id, security_token=security_token).first()
        if user is None:
            raise UserDoesNotExist(message=USER_DOES_NOT_EXIST_OR_WAS_DELETED_MESSAGE)
        return user

    @classmethod
    def update(cls, user: UserModel, **kwargs) -> UserModel:
        for field, value in kwargs.items():
            setattr(user, field, value)
        cls.save(user)
        return user

    @classmethod
    def get_by_email(cls, email: str) -> UserModel:
        return User.objects.get(email=email)

    @classmethod
    def delete_by_id(cls, user_id: UUID) -> tuple:
        user = cls.get_by_id(user_id)
        return user.delete()

    @classmethod
    def delete_users_with_unfinished_registration(cls) -> None:
        unregistered_users = User.objects.filter(
            is_active=False, security_token_expiration_time__lte=now()
        )
        unregistered_users.delete()


class PaymentProviderUserRepository:
    @classmethod
    def save(cls, payment_provider_user: PaymentProviderUser) -> None:
        payment_provider_user.save()
