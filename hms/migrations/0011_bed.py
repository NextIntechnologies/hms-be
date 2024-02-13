# Generated by Django 5.0.1 on 2024-02-11 15:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0010_inventry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('roomNumber', models.CharField(max_length=200)),
                ('roomtype', models.IntegerField(max_length=200)),
                ('admissionDate', models.CharField(max_length=200)),
                ('dischargeDate', models.CharField(max_length=200)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hms.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hms.patient')),
            ],
        ),
    ]
