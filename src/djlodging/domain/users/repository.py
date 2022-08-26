from django.core.exceptions import ValidationError

from djlodging.domain.users.models import User


class UserRepository:
    @classmethod
    def save(cls, user):
        user.save()

    @classmethod
    def get_by_id(cls, user_id) -> User:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("user_id is invalid")

    @classmethod
    def get_by_security_token(cls, security_token) -> User:
        try:
            return User.objects.get(security_token=security_token)
        except User.DoesNotExist:
            raise ValidationError("Such user does not exist")

    @classmethod
    def update(cls, user: User, **kwargs) -> User:
        for field, value in kwargs.items():
            setattr(user, field, value)
        cls.save(user)
        return user

    @classmethod
    def get_by_email(cls, email: str) -> User:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Wrong email!")


class PaymentProviderUserRepository:
    @classmethod
    def save(cls, payment_provider_user):
        payment_provider_user.save()
