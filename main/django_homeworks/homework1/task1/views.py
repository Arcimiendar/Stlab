from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

from .models import Shop


class ShopsView(View):
    def get(self, request):

        return render(request, "shop.html", context={'shops': Shop.objects.all()})

    def post(self, request):

        return redirect(f'{request.POST.get("shop")}/')


class ShopDetailView(DetailView):

    model = Shop
