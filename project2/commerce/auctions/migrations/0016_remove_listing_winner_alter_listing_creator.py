# Generated by Django 4.1.7 on 2023-02-28 07:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0015_alter_listing_creator_alter_listing_winner"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listing",
            name="winner",
        ),
        migrations.AlterField(
            model_name="listing",
            name="creator",
            field=models.CharField(max_length=32),
        ),
    ]
