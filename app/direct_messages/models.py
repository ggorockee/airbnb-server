from django.conf import settings
from django.db import models

from common.models import CommonModel


class ChattingRoom(CommonModel):
    """Room Model Definition"""

    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return "Chatting Room. (TOBE: Number of User)"


class Message(CommonModel):
    """Message Model Definition"""

    text = models.TextField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    chatting_room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user} says: {self.text}"
