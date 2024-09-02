from django.contrib.auth import get_user_model
from rest_framework import serializers


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "username",
            "avatar",
        ]


class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = [
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        ]
        read_only_fields = [
            "groups",
            "user_permissions",
            "last_login",
        ]


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "avatar",
            "username",
            "email",
            "is_host",
            "gender",
            "language",
            "currency",
        ]
