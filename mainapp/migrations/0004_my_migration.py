# Generated by Django 4.0.4 on 2022-05-26 13:35

from django.db import migrations


def forwards_func(apps, schema_editor):
    # Get model
    Human = apps.get_model("mainapp", "Human")
    # Create model's objects
    Human.objects.create(
        first_name="John",
        last_name="Lennon",
    )
    Human.objects.create(
        first_name="Arnold",
        last_name="Schwarzenegger",
    )


def reverse_func(apps, schema_editor):
    # Get model
    Human = apps.get_model("mainapp", "Human")
    # Delete objects
    Human.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('mainapp', '0003_human_migratemodel_worker'),
    ]

    operations = [migrations.RunPython(forwards_func, reverse_func), ]
