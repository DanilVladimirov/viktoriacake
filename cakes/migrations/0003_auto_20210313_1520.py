# Generated by Django 3.1.7 on 2021-03-13 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakes', '0002_remove_decoration_diameter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cake',
            name='img',
            field=models.ImageField(default=None, upload_to='cakes/'),
        ),
    ]
