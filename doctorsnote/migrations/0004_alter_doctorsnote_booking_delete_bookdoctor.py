# Generated by Django 5.1.6 on 2025-02-14 01:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
        ('doctorsnote', '0003_remove_doctorsnote_doctor_remove_doctorsnote_patient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorsnote',
            name='booking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.bookdoctor'),
        ),
        migrations.DeleteModel(
            name='BookDoctor',
        ),
    ]
