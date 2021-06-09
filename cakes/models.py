from django.contrib.auth.models import User
from django.db import models


class CakeDiameters(models.Model):
    diameter = models.IntegerField(default=0.0)
    coefficient = models.FloatField(default=0.0)

    def __str__(self):
        return f'name: {self.diameter}'


class Biscuit(models.Model):
    name = models.CharField(max_length=100, default='Noname Biscuit')
    cost = models.FloatField(default=0.0)
    img = models.ImageField(upload_to='biscuit/', blank=True)
    weight = models.FloatField(default=0.0)
    desc = models.TextField(default='Опис')

    def __str__(self):
        return f'name: {self.name}'


class Filling(models.Model):
    name = models.CharField(max_length=100, default='Noname Filling')
    cost = models.FloatField(default=0.0)
    img = models.ImageField(upload_to='fillings/', blank=True)
    weight = models.FloatField(default=0.0)
    desc = models.TextField(default='Опис')

    def __str__(self):
        return f'name: {self.name}'


class Cream(models.Model):
    name = models.CharField(max_length=100, default='Noname Cream')
    cost = models.FloatField(default=0.0)
    img = models.ImageField(upload_to='creams/', blank=True)
    weight = models.FloatField(default=0.0)
    desc = models.TextField(default='Опис')

    def __str__(self):
        return f'name: {self.name}'


class Decoration(models.Model):
    name = models.CharField(max_length=100, default='Noname Decor')
    cost = models.FloatField(default=0.0)
    img = models.ImageField(upload_to='decors/', blank=True)
    desc = models.TextField(default='Опис')

    def __str__(self):
        return f'name: {self.name}'


class Cake(models.Model):
    name = models.CharField(max_length=100, default='Noname Cake')
    cost = models.FloatField(default=0.0)
    img = models.ImageField(upload_to='cakes/', default=None, blank=True)
    weight = models.FloatField(default=0.0)
    diameter = models.ForeignKey(CakeDiameters, on_delete=models.CASCADE, default=None, blank=True)
    biscuit = models.ForeignKey(Biscuit, on_delete=models.CASCADE, default=None)
    filling = models.ForeignKey(Filling, on_delete=models.CASCADE, default=None)
    cream = models.ForeignKey(Cream, on_delete=models.CASCADE, default=None)
    decoration = models.ForeignKey(Decoration, on_delete=models.CASCADE, default=None)
    desc = models.TextField(default='Опис')

    def __str__(self):
        if self.name == 'Кастомний':
            return f'name: {self.name} #{self.id}'
        else:
            return f'name: {self.name}'

    def price(self):
        return (self.biscuit.cost + self.filling.cost + self.cream.cost + self.decoration.cost) * self.diameter.coefficient

    def total_weight(self):
        return round((self.biscuit.weight + self.filling.weight + self.cream.weight) * self.diameter.coefficient)


class Orders(models.Model):
    cakes = models.ManyToManyField(Cake)
    name = models.CharField(max_length=200, default="noname")
    surname = models.CharField(max_length=200, default="nosur")
    telephone = models.CharField(max_length=20, default="000-000-0000")
    address = models.CharField(max_length=400, default="no addr")
    comment = models.TextField(default="-")


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cakes = models.ManyToManyField(Cake)

    def __str__(self):
        return f'{self.user.username}'


class Recommended(models.Model):
    diameter = models.ForeignKey(CakeDiameters, on_delete=models.CASCADE, default=None, blank=True)
    biscuit = models.ForeignKey(Biscuit, on_delete=models.CASCADE, default=None)
    filling = models.ForeignKey(Filling, on_delete=models.CASCADE, default=None)
    cream = models.ForeignKey(Cream, on_delete=models.CASCADE, default=None)
    decoration = models.ForeignKey(Decoration, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'#{self.id}'


class Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=400)
