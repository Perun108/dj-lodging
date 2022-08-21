from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import PermissionDenied

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
    def confirm_registration(cls, registration_token):
        user = UserRepository.get_by_registration_token(registration_token)
        user.is_active = True
        user.registration_token = ""
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
