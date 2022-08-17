import uuid

from django.db import models


class BaseModel(models.Model):
    """Base model for all models in djlodging"""

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Base model configs."""

        abstract = True
