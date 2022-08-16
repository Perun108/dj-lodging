from djbooking.domain.users.repository import UserRepository

from ..domain.users.models import User


class UserService:
    @classmethod
    def create(cls, **kwargs):
        password = kwargs.pop("password")
        user = User(**kwargs)
        user.set_password(password)
        UserRepository.save(user)
        return user
