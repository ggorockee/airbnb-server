from rest_framework import serializers

from categories.models import Category
from categories.serializers import CategorySerializer
from experiences.models import Perk, Experience
from users.serializers import TinyUserSerializer


class PerksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class CreateExperienceSerializer(serializers.ModelSerializer):
    perks = serializers.ListField(required=False)
    start = serializers.DateField()
    end = serializers.DateField()
    category = serializers.CharField(
        max_length=15,
        required=False,
    )

    class Meta:
        model = Experience
        fields = [
            "id",
            "perks",
            "category",
            "country",  # default: korea
            "city",  # default: seoul
            "name",
            "price",
            "address",
            "start",
            "end",
            "description",
        ]
        extra_kwargs = {}

    def validate_category(self, value):
        # null, "room", "experience"
        category_choices = getattr(Category, "CategoryKindChoices")
        check_list = [category for category in category_choices]
        check_list.append(None)

        if value not in check_list:
            raise serializers.ValidationError(
                "Category value is null or Room or Experience"
            )
        return value


class ExperienceDetailSerializer(serializers.ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    perks = PerksSerializer(many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Experience
        fields = [
            "id",
            "host",
            "perks",
            "category",
            "created_at",
            "updated_at",
            "country",
            "city",
            "name",
            "price",
            "address",
            "start",
            "end",
            "description",
        ]
        extra_kwargs = {
            "host": {"read_only": True},
        }
