from rest_framework import serializers

from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from reviews.seirializers import ReviewsSerializer
from rooms.models import Amenity, Room
from users.serializers import TinyUserSerializer
from wishlists.models import Wishlist


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = [
            "id",
            "name",
            "description",
        ]


class RoomDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(
        read_only=True,
    )
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    reviews = ReviewsSerializer(
        many=True,
        read_only=True,
    )
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Room
        fields = "__all__"

    @staticmethod
    def get_rating(room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def create(self, validated_data):
        return Room.objects.create(**validated_data)


class RoomsSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
            "is_liked",
        ]

    @staticmethod
    def get_rating(room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(user=request.user, rooms__id=room.id).exists()
