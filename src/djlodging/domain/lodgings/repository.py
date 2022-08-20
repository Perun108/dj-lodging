from django.core.exceptions import ValidationError

from djlodging.domain.users.models import User


class UserRepository:
    @classmethod
    def save(cls, user):
        user.save()

    @classmethod
    def get_by_id(cls, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("user_id is invalid")

    @classmethod
    def get_by_registration_token(cls, registration_token) -> User:
        try:
            return User.objects.get(registration_token=registration_token)
        except User.DoesNotExist:
            raise ValidationError("Such user does not exist")
