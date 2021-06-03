# Generated by Django 3.1.7 on 2021-04-26 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cakes', '0010_auto_20210426_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cake',
            name='diameter',
        ),
        migrations.AddField(
            model_name='cake',
            name='diameter',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='cakes.cakediameters'),
        ),
    ]