# Generated by Django 5.1 on 2024-08-29 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0003_room_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="amenity",
            options={"verbose_name_plural": "Amenities"},
        ),
    ]
