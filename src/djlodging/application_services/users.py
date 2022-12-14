from uuid import UUID, uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.timezone import now, timedelta

from djlodging.application_services.exceptions import RegistrationTimePassed
from djlodging.application_services.helpers import check_staff_permissions
from djlodging.domain.core.base_exceptions import DjLodgingValidationError
from djlodging.domain.users.models import PaymentProviderUser
from djlodging.domain.users.models import User as UserModel
from djlodging.domain.users.repository import PaymentProviderUserRepository, UserRepository
from djlodging.infrastructure.jobs.celery_tasks import (
    delete_unregistered_user_after_security_token_expired,
    send_change_email_link_task,
    send_change_password_link_task,
    send_confirmation_link_task,
)
from djlodging.infrastructure.providers.payments import payment_provider

User = get_user_model()


class UserService:
    @classmethod
    def create(cls, **kwargs) -> UserModel:
        password = kwargs.pop("password")
        user = User(**kwargs)
        validate_password(password, user)
        user.set_password(password)
        user.security_token_expiration_time = now() + timedelta(
            hours=settings.SECURITY_TOKEN_LIFE_TIME_IN_HOURS
        )
        UserRepository.save(user)
        send_confirmation_link_task(user.email, user.security_token)
        return user

    @classmethod
    def confirm_registration(cls, user_id: UUID, security_token: UUID) -> UserModel:
        user = UserRepository.get_user_by_id_and_security_token(user_id, security_token)

        if user.security_token_expiration_time < now():
            delete_unregistered_user_after_security_token_expired.apply_async(args=[user_id])
            raise RegistrationTimePassed

        user.security_token = ""
        user.is_active = True
        UserRepository.save(user)
        PaymentProviderUserService.create(user)
        return user

    @classmethod
    def make_user_partner(
        cls, user: UserModel, first_name: str, last_name: str, phone_number: str
    ) -> UserModel:
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.is_partner = True
        UserRepository.save(user)
        return user

    @classmethod
    def change_password(cls, user: UserModel, old_password: str, new_password: str) -> UserModel:
        if not user.check_password(old_password):
            raise DjLodgingValidationError("Wrong password!")
        user.set_password(new_password)
        UserRepository.save(user)
        return user

    @classmethod
    def send_forgot_password_link(cls, email: str) -> None:
        user = UserRepository.get_by_email(email)
        security_token = uuid4()
        UserRepository.update(user, security_token=security_token)
        send_change_password_link_task(user.email, security_token)

    @classmethod
    def confirm_reset_password(cls, security_token: UUID, email: str, new_password: str) -> None:
        user = UserRepository.get_user_by_security_token_and_email(security_token, email)
        user.security_token = ""
        user.set_password(new_password)
        UserRepository.save(user)

    @classmethod
    def send_change_email_link(cls, user: UserModel, new_email: str) -> None:
        security_token = uuid4()
        UserRepository.update(user, security_token=security_token)
        send_change_email_link_task(new_email, security_token)

    @classmethod
    def change_email(cls, security_token: UUID, new_email: str) -> None:
        user = UserRepository.get_user_by_security_token(security_token)
        user.email = new_email
        user.security_token = ""
        UserRepository.save(user)

    @classmethod
    def update_by_admin(cls, actor: UserModel, user_id: UUID, **kwargs) -> UserModel:
        check_staff_permissions(actor)
        user = UserRepository.get_by_id(user_id)
        return cls.update(user, **kwargs)

    @classmethod
    def update(cls, user: UserModel, **kwargs) -> UserModel:
        for field, value in kwargs.items():
            setattr(user, field, value)
        UserRepository.save(user)
        return user


class PaymentProviderUserService:
    @classmethod
    def create(cls, user: UserModel) -> PaymentProviderUser:
        customer = payment_provider.create_payment_user(email=user.email)
        payment_provider_user = PaymentProviderUser(user=user, customer_id=customer.id)
        PaymentProviderUserRepository.save(payment_provider_user)
        return payment_provider_user
