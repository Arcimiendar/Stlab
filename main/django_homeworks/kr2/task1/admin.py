from django.contrib import admin
from .models import Student, Teacher, Note

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Note)

# Register your models here.
