# Generated by Django 4.1.7 on 2023-02-27 11:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0011_alter_listing_creator"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="creator",
            field=models.CharField(max_length=32),
        ),
    ]
