from rest_framework import serializers

from experiences.models import Perk


class PerksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"
