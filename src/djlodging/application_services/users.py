from django.contrib.auth.password_validation import validate_password

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
