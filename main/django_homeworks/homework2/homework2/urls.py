"""homework2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from task2 import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, base_name='user')
router.register('departments', views.DepartmentViewSet, base_name='department')
router.register('shops', views.ShopViewSet, base_name='shop')
router.register('items', views.ItemViewSet, base_name='item')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('unsold_items/', views.UnsoldItemApiView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
