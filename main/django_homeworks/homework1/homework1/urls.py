"""homework1 URL Configuration

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
from django.urls import path

from task1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ShopsView.as_view(), name='index'),
    path('shops/<int:pk>/', views.ShopDetailView.as_view(), name='shopDetail'),
    path('shops/<int:pk>/more', views.ShopDetailMoreView.as_view()),
    path('shops/<int:pk>/edit', views.ShopUpdate.as_view()),
    path('shops/<int:pk>/delete', views.ShopDelete.as_view()),
    path('shops/<int:pk>/create', views.ShopCreate.as_view()),
    path('items/<int:pk>/edit', views.ItemUpdate.as_view()),
    path('items/<int:pk>/delete', views.ItemDelete.as_view()),
    path('items/<int:department_id>/create', views.ItemCreate.as_view()),
    path('departments/<int:pk>/edit', views.DepartmentUpdate.as_view()),
    path('departments/<int:pk>/delete', views.DepartmentDelete.as_view()),
    path('departments/<int:shop_id>/create', views.DepartmentCreate.as_view()),
    path('filter/item/<int:number>', views.ItemFilterView.as_view()),
    path('filter/shop/<int:number>', views.ShopFilterView.as_view())
]
