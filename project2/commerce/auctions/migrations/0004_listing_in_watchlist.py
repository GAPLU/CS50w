# Generated by Django 4.1.7 on 2023-02-26 12:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0003_alter_listing_image_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="in_watchlist",
            field=models.BooleanField(default=False),
        ),
    ]