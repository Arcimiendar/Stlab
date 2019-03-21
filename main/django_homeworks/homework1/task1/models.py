from django.db import models
from django.contrib.postgres import fields as postgres_fields


class Shop(models.Model):

    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    staff_amount = models.IntegerField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Department(models.Model):

    sphere = models.CharField(max_length=200)
    staff_amount = models.IntegerField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,
                             related_name="departments", verbose_name="Shop")

    def __str__(self):
        return f'{self.shop.name}: {self.sphere}'

    def __repr__(self):
        return self.__str__()


class Item(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    is_sold = models.BooleanField(null=False)
    comments = postgres_fields.ArrayField(
        models.CharField(max_length=200, blank=True, null=True), blank=True
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f'{self.department.shop.name}: {self.department.sphere}: {self.name}'

    def __repr__(self):
        return self.__str__()


class Statistics(models.Model):

    url = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.amount} times on {self.url}'
