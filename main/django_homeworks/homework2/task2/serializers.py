from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Item, Department, Shop
from .serializer_fields import DepartmentStringField


class ItemSerializerForUserWithoutNameAndSurname(serializers.HyperlinkedModelSerializer):
    department = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Item
        fields = (
            'name', 'is_sold',
            'description', 'department', 'comments'
        )


class ItemFullSerializer(ItemSerializerForUserWithoutNameAndSurname):
    class Meta:
        model = Item
        fields = (
            'name', 'price', 'is_sold',
            'description', 'department', 'comments'
        )


class ItemPartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = (
            'name', 'is_sold',
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
           'username', 'first_name', 'last_name',
           'email', 'is_staff', 'is_active'
        )


class DepartmentSerializerForUserWithoutNameAndSurname(serializers.HyperlinkedModelSerializer):
    shop = serializers.StringRelatedField(many=False, read_only=True)
    items = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Department
        fields = (
            'sphere', 'shop', 'items'
        )


class DepartmentSerializerForUserWithNameAndSurname(DepartmentSerializerForUserWithoutNameAndSurname):
    class Meta:
        model = Department
        fields = (
            'sphere', 'staff_amount', 'shop', 'items'
        )


class DepartmentSerializer(DepartmentSerializerForUserWithNameAndSurname):
    pass


class ShopSerializerForUserWithoutNameAndSurname(serializers.HyperlinkedModelSerializer):
    departments = DepartmentStringField(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = (
            'name', 'address', 'departments'
        )


class ShopSerializerForUserWithNameAndSurname(ShopSerializerForUserWithoutNameAndSurname):
    class Meta:
        model = Shop
        fields = (
            'name', 'address', 'departments', 'staff_amount'
        )


class ShopSerializer(ShopSerializerForUserWithNameAndSurname):
    departments = serializers.StringRelatedField(many=True, read_only=True)

