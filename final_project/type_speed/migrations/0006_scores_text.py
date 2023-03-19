# Generated by Django 4.1.7 on 2023-03-19 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("type_speed", "0005_scores_custom"),
    ]

    operations = [
        migrations.AddField(
            model_name="scores",
            name="text",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="type_speed.customtext",
            ),
        ),
    ]
