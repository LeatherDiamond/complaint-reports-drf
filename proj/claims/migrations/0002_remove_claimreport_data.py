# Generated by Django 4.2.13 on 2024-05-16 11:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("claims", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="claimreport",
            name="data",
        ),
    ]
