# Generated by Django 5.0.2 on 2024-02-15 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carsite', '0007_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(default='media/photos/default.jpg', upload_to='media/photos/'),
        ),
    ]
