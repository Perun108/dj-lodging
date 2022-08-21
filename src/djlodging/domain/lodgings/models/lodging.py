from django.contrib.auth import get_user_model
from django.db import models

from djlodging.domain.core.base_models import BaseModel

from .city import City

User = get_user_model()


class Lodging(BaseModel):
    class Type(models.TextChoices):
        apartment = "apartment", "Apartment"
        home = "home", "Home"
        hotel = "hotel", "Hotel"
        other = "other", "Other"

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=Type.choices)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lodging")
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    district = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.city} {self.street} {self.house_number}"


def images_folder(instance, filename):
    return f"{instance.lodging}/{filename}"


class LodgingImage(BaseModel):
    image = models.ImageField(upload_to=images_folder)
    lodging = models.ForeignKey(Lodging, on_delete=models.CASCADE, related_name="image")

    def __str__(self):
        return str(self.id)
