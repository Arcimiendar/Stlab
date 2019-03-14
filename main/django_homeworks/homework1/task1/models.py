from django.db import models
from django.contrib.postgres import fields as postgres_fields


class Shop(models.Model):

    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    staff_amount = models.IntegerField()

    def __str__(self):
        return self.name


class Department(models.Model):

    sphere = models.CharField(max_length=200)
    staff_amount = models.IntegerField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.shop.name}: {self.sphere}'


class Item(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    is_sold = models.BooleanField()
    comments = postgres_fields.ArrayField(
        models.CharField(max_length=200, blank=True, null=True)
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.department.shop.name}: {self.department.sphere}: {self.name}'
