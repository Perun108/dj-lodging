from django.db import models

from djlodging.domain.core.base_models import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
