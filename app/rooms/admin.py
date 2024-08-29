from django.contrib import admin

from rooms.models import Room, Amenity


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "kind",
        "owner",
        "total_amenities",
    ]

    list_filter = [
        "city",
        "price",
        "rooms",
        "toilets",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    ]


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_filter = [
        "name",
        "description",
        "created_at",
        "updated_at",
    ]
