from uuid import UUID, uuid4

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import PermissionDenied, ValidationError

from djlodging.application_services.email import EmailService
from djlodging.domain.users.repository import UserRepository

from ..domain.users.models import User


class UserService:
    @classmethod
    def create(cls, **kwargs):
        password = kwargs.pop("password")
        user = User(**kwargs)
        validate_password(password, user)
        user.set_password(password)
        UserRepository.save(user)
        return user

    @classmethod
    def confirm_registration(cls, security_token):
        user = UserRepository.get_by_security_token(security_token)
        user.is_active = True
        user.security_token = ""
        UserRepository.save(user)
        return user

    @classmethod
    def make_user_partner(cls, actor, user_id, first_name, last_name, phone_number):
        user = UserRepository.get_by_id(user_id)
        if actor != user:
            raise PermissionDenied
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.is_partner = True
        UserRepository.save(user)
        return user

    @classmethod
    def change_password(cls, user: User, old_password: str, new_password: str) -> User:
        if not user.check_password(old_password):
            raise ValidationError("Wrong password!")
        user.set_password(new_password)
        UserRepository.save(user)
        return user

    @classmethod
    def send_forgot_password_link(cls, email: str) -> None:
        user = UserRepository.get_by_email(email)
        security_token = uuid4()
        UserRepository.update(user, security_token=security_token)
        EmailService.send_change_password_link(user.email, security_token)

    @classmethod
    def confirm_reset_password(cls, token: UUID) -> None:
        user = UserRepository.get_by_security_token(token)
        user.security_token = ""
        UserRepository.save(user)
