# Generated by Django 4.1.7 on 2023-02-28 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0017_remove_listing_creator"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="creator",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_listings",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="listing",
            name="winner",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="won_listings",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
