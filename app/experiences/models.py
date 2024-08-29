from django.db import models
from django.conf import settings

from common.models import CommonModel


class Experience(CommonModel):
    """Experience Model Definition"""

    country = models.CharField(
        max_length=50,
        default="korea",
    )

    city = models.CharField(
        max_length=80,
        default="seoul",
    )

    name = models.CharField(
        max_length=250,
    )

    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=250,
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField(
        blank=True,
        null=True,
    )
    perks = models.ManyToManyField(
        "experiences.Perk",
    )

    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    """What is included on an Experience"""

    name = models.CharField(
        max_length=100,
    )
    details = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    explanation = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
