from rest_framework import serializers

from categories.serializers import CategorySerializer
from rooms.models import Amenity, Room
from users.serializers import TinyUserSerializer


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = [
            "id",
            "name",
            "description",
        ]


class RoomDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer()
    amenities = AmenitySerializer(
        many=True,
    )
    category = CategorySerializer()

    class Meta:
        model = Room
        fields = "__all__"


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "country",
            "city",
            "price",
        ]
