from django.db import models

from djlodging.domain.core.base_models import BaseModel

from .country import Country


class City(BaseModel):
    country = models.ForeignKey(Country, related_name="city", on_delete=models.CASCADE)
    region = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"
