from typing import Any

from django.views import View
from rest_framework import permissions
from rest_framework.request import Request


class IsStaff(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_staff


class IsUserWithNameAndSurname(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.user.is_authenticated and len(request.user.last_name) and len(request.user.first_name) and \
                request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False


class IsUserWithoutNameAndSurname(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.user.is_authenticated and not len(request.user.last_name) and not len(request.user.first_name) and \
                request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
