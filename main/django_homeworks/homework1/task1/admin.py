from django.contrib import admin
from .models import Department, Shop, Item, Statistics

admin.site.register(Item)
admin.site.register(Shop)
admin.site.register(Department)
admin.site.register(Statistics)

# Register your models here.
