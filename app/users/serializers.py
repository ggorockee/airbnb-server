from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "username",
            "avatar",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()

    def validate(self, data):
        request = self.context.get("request")
        input_password = data.get("old_password")
        if not request.user.check_password(input_password):
            raise serializers.ValidationError("Wrong password")

        if data.get("new_password1") != data.get("new_password2"):
            raise serializers.ValidationError("The passwords entered must be the same.")

        return data


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


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        request = self.context.get("request")
        email = data.get("email")
        password = data.get("password")

        user = authenticate(
            request,
            username=email,
            password=password,
        )

        data["user"] = user

        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        return data
