# Generated by Django 5.0.1 on 2024-02-11 19:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0014_rename_roomtype_bed_roomtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('department', models.CharField(max_length=200)),
                ('admissionDate', models.CharField(max_length=200)),
                ('dischargeDate', models.CharField(max_length=200)),
                ('costOfTreatment', models.IntegerField(max_length=200)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hms.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hms.patient')),
            ],
        ),
    ]
