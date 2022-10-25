from django.contrib.auth import get_user_model
from django.db import models

from djlodging.domain.core.base_models import BaseModel

from .city import City

User = get_user_model()


class Lodging(BaseModel):
    class Kind(models.TextChoices):
        APARTMENT = "apartment", "Apartment"
        HOME = "home", "Home"
        HOTEL = "hotel", "Hotel"
        OTHER = "other", "Other"

    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=50, choices=Kind.choices)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lodging")
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    district = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    number_of_people = models.PositiveSmallIntegerField(default=1)
    number_of_rooms = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.name} in {self.city}"


def images_folder(instance, filename):
    return f"{instance.lodging}/{filename}"


class LodgingImage(BaseModel):
    image = models.ImageField(upload_to=images_folder)
    lodging = models.ForeignKey(Lodging, on_delete=models.CASCADE, related_name="image")

    def __str__(self):
        return str(self.id)
