# Generated by Django 3.1.7 on 2021-06-21 09:34

import cakes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakes', '0016_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biscuit',
            name='img',
            field=models.ImageField(blank=True, upload_to=cakes.models.file_path),
        ),
        migrations.AlterField(
            model_name='cake',
            name='img',
            field=models.ImageField(blank=True, default=None, upload_to=cakes.models.file_path),
        ),
        migrations.AlterField(
            model_name='cream',
            name='img',
            field=models.ImageField(blank=True, upload_to=cakes.models.file_path),
        ),
        migrations.AlterField(
            model_name='decoration',
            name='img',
            field=models.ImageField(blank=True, upload_to=cakes.models.file_path),
        ),
        migrations.AlterField(
            model_name='filling',
            name='img',
            field=models.ImageField(blank=True, upload_to=cakes.models.file_path),
        ),
    ]
