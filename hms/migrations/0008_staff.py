# Generated by Django 5.0.1 on 2024-02-11 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0007_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
    ]