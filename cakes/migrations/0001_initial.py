# Generated by Django 3.1.7 on 2021-03-13 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Biscuit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Noname Biscuit', max_length=100)),
                ('cost', models.FloatField(default=0.0)),
                ('img', models.ImageField(upload_to='biscuit/')),
                ('weight', models.FloatField(default=0.0)),
                ('diameter', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Noname Cream', max_length=100)),
                ('cost', models.FloatField(default=0.0)),
                ('img', models.ImageField(upload_to='creams/')),
                ('weight', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Decoration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Noname Decor', max_length=100)),
                ('cost', models.FloatField(default=0.0)),
                ('img', models.ImageField(upload_to='decors/')),
                ('diameter', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Filling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Noname Filling', max_length=100)),
                ('cost', models.FloatField(default=0.0)),
                ('img', models.ImageField(upload_to='fillings/')),
                ('weight', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Noname Cake', max_length=100)),
                ('cost', models.FloatField(default=0.0)),
                ('img', models.ImageField(upload_to='cakes/')),
                ('weight', models.FloatField(default=0.0)),
                ('diameter', models.IntegerField(default=0)),
                ('biscuit', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cakes.biscuit')),
                ('cream', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cakes.cream')),
                ('decoration', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cakes.decoration')),
                ('filling', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cakes.filling')),
            ],
        ),
    ]