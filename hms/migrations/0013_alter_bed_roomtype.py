# Generated by Django 5.0.1 on 2024-02-11 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0012_rename_admissiondate_bed_allotmentdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bed',
            name='roomtype',
            field=models.CharField(max_length=200),
        ),
    ]
