# Generated by Django 5.0.1 on 2024-03-11 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0016_billing_bill'),
    ]

    operations = [
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=200)),
                ('otp', models.CharField(max_length=200)),
            ],
        ),
    ]