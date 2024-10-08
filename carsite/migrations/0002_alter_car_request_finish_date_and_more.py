# Generated by Django 5.0.2 on 2024-02-23 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_request',
            name='finish_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='car_request',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='car_request',
            name='start_date',
            field=models.DateField(blank=True),
        ),
    ]
