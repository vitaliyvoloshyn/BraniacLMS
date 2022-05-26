# Generated by Django 4.0.4 on 2022-05-26 14:32

from django.db import migrations


def transfer_data_to_dest_model(apps, schema_editor):
    Data = apps.get_model("mainapp", "MigrateModel")
    DestModel = apps.get_model("mainapp", "Worker")
    for i in Data.objects.all():
        DestModel.objects.create(first_name=i.name)


class Migration(migrations.Migration):
    dependencies = [
        ('mainapp', '0006_deleting_data_in_original_model'),
    ]

    operations = [migrations.RunPython(transfer_data_to_dest_model), ]
