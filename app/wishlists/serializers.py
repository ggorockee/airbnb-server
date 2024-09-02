from rest_framework import serializers

from rooms.serializers import RoomsSerializer
from wishlists.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    rooms = RoomsSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = [
            "name",
            "rooms",
        ]
