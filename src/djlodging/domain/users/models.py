from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models

from djlodging.domain.core.base_models import BaseModel


class User(AbstractUser, BaseModel):
    """Users in djlodging"""

    class Gender(models.TextChoices):
        male = "male", "Male"
        female = "female", "Female"
        not_disclosed = "not_disclosed", "Not disclosed"

    is_user = models.BooleanField(default=True)
    is_partner = models.BooleanField(default=False)
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    email = models.EmailField(validators=[EmailValidator()], unique=True)
    phone_number = models.CharField(max_length=16, blank=True)
    username = models.CharField(max_length=60, blank=True, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=20, blank=True, choices=Gender.choices)
    registration_token = models.CharField(max_length=100, blank=True, default=uuid4)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email or self.username

    def save(self, *args, **kwargs):
        if self.username == "":
            self.username = self.email
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
