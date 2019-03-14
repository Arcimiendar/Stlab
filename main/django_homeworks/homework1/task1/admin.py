from django.contrib import admin
from .models import Department, Shop, Item

admin.site.register(Item)
admin.site.register(Shop)
admin.site.register(Department)

# Register your models here.
