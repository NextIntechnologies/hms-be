# Generated by Django 5.0.1 on 2024-02-01 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0002_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='dob',
            field=models.CharField(max_length=200),
        ),
    ]
