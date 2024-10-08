from django.db import models
from django.conf import settings
from django.db.models import CharField

from common.models import CommonModel


class Room(CommonModel):
    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(max_length=180)

    country = models.CharField(
        max_length=50,
        default="korea",
    )
    city = models.CharField(
        max_length=80,
        default="seoul",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(
        max_length=250,
    )
    pet_friendly = models.BooleanField(
        default=False,
    )
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rooms",
    )

    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
    )

    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )

    def __str__(self) -> CharField:
        return self.name

    def total_amenities(self):
        return self.amenities.count()

    def rating(self):
        count = self.reviews.count()
        if count == 0:
            return 0

        total_rating = 0
        for review in self.reviews.all().values("rating"):
            total_rating += review["rating"]
        return round(total_rating / count, 2)


class Amenity(CommonModel):
    """Amenity Definition"""

    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self) -> CharField:
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
