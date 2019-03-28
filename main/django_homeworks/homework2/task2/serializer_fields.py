from rest_framework import serializers
from .models import Department


class DepartmentStringField(serializers.StringRelatedField):
    def to_representation(self, value: Department):
        if value.items.count() == 0:
            return None
        return super().to_representation(value)
