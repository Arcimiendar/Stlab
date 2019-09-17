from django.contrib import admin
from .models import Item, Department, Statistics, Shop

admin.site.register(Shop)
admin.site.register(Item)
admin.site.register(Department)
admin.site.register(Statistics)
