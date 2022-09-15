from django.contrib.auth import get_user_model
from django.db import models

from djlodging.domain.core.base_models import BaseModel
from djlodging.domain.lodgings.models import Lodging

User = get_user_model()


class Booking(BaseModel):
    class Status(models.TextChoices):
        PAYMENT_PENDING = "payment_pending", "Payment pending"
        PAID = "paid", "Paid"
        CANCELED = "canceled", "Canceled"

    lodging = models.ForeignKey(
        Lodging, on_delete=models.SET_NULL, null=True, related_name="booking"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking")
    date_from = models.DateField()
    date_to = models.DateField()
    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.PAYMENT_PENDING
    )
    payment_intent_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return (
            f"{self.user.email} | {self.lodging.name} in {self.lodging.city} | "
            + f"({self.date_from} - {self.date_to})"
        )
