# Generated by Django 4.1.7 on 2023-02-27 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0010_comments_listing_listing_creator_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="creator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
