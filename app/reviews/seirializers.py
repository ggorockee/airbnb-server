from rest_framework import serializers

from reviews.models import Review
from users.serializers import TinyUserSerializer


class ReviewsSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "payload",
            "rating",
        ]
