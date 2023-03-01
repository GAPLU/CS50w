# Generated by Django 4.1.7 on 2023-03-01 09:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0033_remove_listing_in_watchlist_watchlist"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category", models.CharField(blank=True, max_length=64)),
            ],
        ),
    ]
