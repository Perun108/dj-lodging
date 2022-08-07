from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, MinLengthValidator
from django.db import models

from djbooking.django_app.base_models import BaseModel


class User(AbstractUser, BaseModel):
    """Users in djbooking"""

    first_name = models.CharField(max_length=255, validators=[MinLengthValidator(2)], blank=True)
    last_name = models.CharField(max_length=255, validators=[MinLengthValidator(2)], blank=True)
    email = models.EmailField(validators=[EmailValidator()], unique=True)
    phone_number = models.CharField(max_length=16, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email or self.username

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
