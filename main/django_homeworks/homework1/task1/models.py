from django.db import models
from django.contrib.postgres import fields as postgres_fields


class Shop(models.Model):

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    staff_amount = models.IntegerField()

    def __str__(self):
        return self.name


class Department(models.Model):

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    sphere = models.CharField(max_length=200)
    staff_amount = models.IntegerField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,
                             related_name="departments", verbose_name="Shop")

    def __str__(self):
        return f'{self.shop.name}: {self.sphere}'


class Item(models.Model):

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    is_sold = models.BooleanField(null=False)
    comments = postgres_fields.ArrayField(
        models.CharField(max_length=200, blank=True, null=True), blank=True
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f'{self.department.shop.name}: {self.department.sphere}: {self.name}'
