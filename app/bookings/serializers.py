from rest_framework import serializers
from django.utils import timezone

from bookings.models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = [
            "check_in",
            "check_out",
            "guests",
        ]

    @staticmethod
    def validate_check_in(value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past")
        return value

    @staticmethod
    def validate_check_out(value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past")
        return value

    def validate(self, data):
        if data.get("check_out") < data.get("check_in"):
            raise serializers.ValidationError(
                "check in should be smaller than check out"
            )

        if Booking.objects.filter(
            check_in__lte=data.get("check_out"),
            check_out__gte=data.get("check_in"),
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of those dates are already taken."
            )
        return data


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        ]
