# Generated by Django 4.1.7 on 2023-02-28 08:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0027_alter_listing_creator_alter_listing_winner"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listing",
            name="winner",
        ),
    ]
