# Generated by Django 4.1.7 on 2023-02-26 12:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0006_alter_listing_image_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="image_url",
            field=models.CharField(max_length=200),
        ),
    ]