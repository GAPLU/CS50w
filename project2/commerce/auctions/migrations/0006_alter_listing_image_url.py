# Generated by Django 4.1.7 on 2023-02-26 12:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_alter_listing_in_watchlist"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="image_url",
            field=models.FilePathField(),
        ),
    ]
