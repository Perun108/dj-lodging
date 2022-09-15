from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

from djlodging.domain.core.base_models import BaseModel

from .lodging import Lodging

User = get_user_model()


class Review(BaseModel):
    lodging = models.ForeignKey(Lodging, on_delete=models.CASCADE, related_name="reviews")

    score = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])

    def __str__(self):
        return f"Review for {self.lodging} with a score {self.score}"
