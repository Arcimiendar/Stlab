from typing import Any

from django.contrib.auth.models import User
from django.db.models import Count, Q
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Item, Shop, Department
from .serializers import ItemFullSerializer, ItemPartSerializer, UserSerializer, \
                         DepartmentSerializer, ShopSerializer, ShopSerializerForUserWithNameAndSurname, \
                         ShopSerializerForUserWithoutNameAndSurname
from .permissions import IsStaff, IsUserWithNameAndSurname, IsUserWithoutNameAndSurname


class UnsoldItemApiView(APIView):

    def get(self, request, detail=False):
        items = Item.objects.filter(is_sold=False)
        data = {'response': '401 permission denied'}, 401

        if request.user.is_superuser:
            data = ItemFullSerializer(
                items, many=True, context={'request': request}
            ).data, 200
        elif request.user.is_anonymous:
            data = ItemPartSerializer(
                items, many=True, context={'request': request}
            ).data, 200

        return Response(*data)

    @action(method=['delete'], detail=False)
    def delete(self, request, detail=False):
        if request.user.is_superuser:
            Item.objects.all().delete()
            return Response({'response': '200ok'})
        else:
            return Response({'response': '401 permission denied'}, 401)


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemFullSerializer
    permission_classes = [IsStaff | IsUserWithNameAndSurname | IsUserWithoutNameAndSurname]

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_sold=False)
        return queryset


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsStaff | IsUserWithNameAndSurname | IsUserWithoutNameAndSurname]

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = queryset.annotate(item_count=Count('items')).filter(item_count__gt=0)
            queryset = queryset.annotate(item_sold=Count('items__is_sold', filter=Q(items__is_sold=True)))\
                .filter(item_sold__lt=1)
        return queryset


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsStaff | IsUserWithNameAndSurname | IsUserWithoutNameAndSurname]

    def get_queryset(self):
        queryset = self.queryset
        # if not self.request.user.is_staff:
            # queryset = queryset.annotate(item_count=Count('departments__items')).filter(item_count__gt=0)
            # queryset = queryset.annotate(
            #     item_sold=Count('departments__items__is_sold', filter=Q(departments__items__is_sold=True))
            # ).filter(item_sold__lt=1)
        return queryset

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ShopSerializer
        elif len(self.request.user.first_name):
            return ShopSerializerForUserWithNameAndSurname
        else:
            return ShopSerializerForUserWithoutNameAndSurname

    def get_serializer(self, *args: Any, **kwargs: Any):
        serializer = super().get_serializer(*args, **kwargs)

        return serializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsStaff]
