# Generated by Django 4.0.4 on 2022-05-26 13:59

from django.db import migrations


def delete_data_from_orig_model(apps, schema_editor):
    Data = apps.get_model("mainapp", "Human")
    for i in Data.objects.all():
        i.firstname = ''


class Migration(migrations.Migration):
    dependencies = [
        ('mainapp', '0005_transferring_data_to_intermediate_model'),
    ]

    operations = [migrations.RunPython(delete_data_from_orig_model), ]
