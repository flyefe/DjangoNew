# Generated by Django 5.0.7 on 2024-07-29 11:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="convert_to_lead",
            field=models.BooleanField(default=False),
        ),
    ]