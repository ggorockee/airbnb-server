from django.db import models

from common.models import CommonModel


class Category(CommonModel):
    """Room and Experience Category"""

    class CategoryKindChoices(models.TextChoices):
        ROOM = "rooms", "Rooms"
        EXPERIENCES = "experiences", "Experiences"

    name = models.CharField(
        max_length=50,
    )
    kind = models.CharField(
        max_length=30,
        choices=CategoryKindChoices.choices,
    )

    def __str__(self):
        return f"{self.kind}: {self.name}"

    class Meta:
        verbose_name_plural = "Categories"
