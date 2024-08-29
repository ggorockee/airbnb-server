from rest_framework import serializers

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # "__all__" : 모든필드
        # exclude = []
        # fields = []
        fields = "__all__"
