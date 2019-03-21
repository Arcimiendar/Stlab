from django.db.models import Q, F, Sum, Count, Max
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView, ListView, FormView, TemplateView

from .models import Shop, Item, Department
from .forms import CompareForm


class ShopsView(View):
    def get(self, request):

        return render(request, "shop.html", context={'shops': Shop.objects.all()})

    def post(self, request):

        return redirect(f'shops/{request.POST.get("shop")}/')


class ShopDetailView(DetailView):

    model = Shop


class ItemUpdate(UpdateView):

    model = Item
    template_name = 'task1/update.html'
    fields = ['name', 'description', 'is_sold', 'price', 'comments', 'department']

    def get_success_url(self):
        return reverse_lazy("shopDetail", args=[self.object.department.shop_id])


class ItemDelete(DeleteView):

    model = Item
    template_name = 'task1/delete.html'

    def get_success_url(self):
        return reverse_lazy("shopDetail", args=[self.object.department.shop_id])


class ItemCreate(CreateView):

    model = Item
    fields = ['name', 'description', 'is_sold', 'price', 'comments']
    template_name = 'task1/create.html'

    def form_valid(self, form):

        self.object = Item(
            department_id=self.kwargs['department_id'], **form.cleaned_data
        )

        self.object.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('shopDetail', args=[self.object.department.shop_id])


class DepartmentUpdate(UpdateView):

    model = Department
    template_name = 'task1/update.html'
    fields = ['sphere', 'staff_amount', 'shop']

    def get_success_url(self):
        return reverse_lazy("shopDetail", args=[self.object.shop_id])


class DepartmentDelete(DeleteView):

    model = Department
    template_name = 'task1/delete.html'

    def get_success_url(self):
        return reverse_lazy("shopDetail", args=[self.object.shop_id])


class DepartmentCreate(CreateView):

    model = Department
    fields = ['sphere', 'staff_amount']
    template_name = 'task1/create.html'

    def form_valid(self, form):

        self.object = Department(
            shop_id=self.kwargs['shop_id'], **form.cleaned_data
        )

        self.object.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('shopDetail', args=[self.object.shop_id])


class ShopUpdate(UpdateView):

    model = Shop
    template_name = 'task1/update.html'
    fields = ['name', 'address', 'staff_amount']

    def get_success_url(self):
        return reverse_lazy("shopDetail", args=[self.object.id])


class ShopDelete(DeleteView):

    model = Shop
    template_name = 'task1/delete.html'

    def get_success_url(self):
        return reverse_lazy("index")


class ShopCreate(CreateView):

    model = Shop
    fields = ['name', 'address', 'staff_amount']
    template_name = 'task1/create.html'

    def get_success_url(self):
        return reverse_lazy('shopDetail', args=[self.object.id])


class ShopDetailMoreView(DetailView):

    template_name = 'task1/shop_more_detail.html'
    model = Shop


class ItemFilterView(ListView):
    model = Item
    template_name = 'task1/objects_list.html'

    def get_queryset(self):

        queryset = super().get_queryset()

        if self.kwargs['number'] == 1:
            queryset = queryset.filter(department__shop__name__istartswith='i')
        elif self.kwargs['number'] == 2:
            queryset = queryset.filter(price__gt=10, department__staff_amount__lt=50)
        elif self.kwargs['number'] == 3:
            queryset = queryset.filter(Q(price__gt=20) | Q(department__shop__staff_amount__gt=50))
        elif self.kwargs['number'] == 4:
            queryset = queryset.filter(Q(department_id=1) | Q(department_id=3) |
                                       Q(department_id=5) | Q(department_id=6))
        elif self.kwargs['number'] == 5:
            queryset = queryset.filter(Q(price__gt=10, name__icontains='a') |
                                       Q(price__lt=20, name__icontains='o'))
        elif self.kwargs['number'] == 6:
            queryset = queryset.filter(price=F('department__staff_amount') + 10)

        return queryset


class ShopFilterView(ListView):
    model = Shop
    template_name = 'task1/objects_list.html'

    def get_queryset(self):

        queryset = super().get_queryset()

        if self.kwargs['number'] == 1:
            queryset = queryset.annotate(departments_staff_sum=Sum('departments__staff_amount')).\
                filter(~Q(staff_amount=F('departments_staff_sum')))
        elif self.kwargs['number'] == 2:
            queryset = queryset.filter(departments__items__price__lt=5).distinct()
        elif self.kwargs['number'] == 3:
            queryset_departments = queryset.annotate(
                number_departments=Count('departments', distinct=True),
                sum_departments_staff_amount=Sum("departments__staff_amount")
            ).order_by('id')
            queryset_items = queryset.annotate(
                max_price=Max('departments__items__price'),
                items_number=Count('departments__items')
            ).values('max_price', 'id', 'items_number').order_by('id')

            queryset = Shop.objects.raw(
                """
                select s.id, s.name, s.address, s.staff_amount, count(d.id) departments_count, 
                sum(d.staff_amount) department_staff, sq.items_count, sq.max_price  
                from task1_shop s 
                inner join task1_department d on s.id = d.shop_id 
                inner join (select s.id, count(i.id) items_count, max(i.price) max_price 
                from task1_shop s 
                inner join task1_department d on s.id = d.shop_id 
                inner join task1_item i on d.id = i.department_id 
                group by s.id) 
                sq on s.id = sq.id group by s.id, s.name, s.address, s.staff_amount, sq.items_count, sq.max_price 
                order by s.id
                """
            )

        elif self.kwargs['number'] == 4:
            queryset = queryset.annotate(
                specific_items=Count('departments__items',
                                     filter=
                                     Q(departments__items__price__lte=10) | Q(departments__items__name__contains='a'))
            )

        return queryset


class CompareView(FormView):

    template_name = 'task1/form_view.html'
    form_class = CompareForm
    success_url = '/'

    def form_valid(self, form):

        context = {}

        departments = Department.objects.annotate(
            sum_sold=Sum("items__price", filter=Q(items__is_sold=True)),
            sum_unsold=Sum("items__price", filter=Q(items__is_sold=False)),
            sum=Sum("items__price"),
            number_sold=Count("items__price", filter=Q(items__is_sold=True)),
            number_unsold=Count("items__price", filter=Q(items__is_sold=False)),
            number=Count("items__price"),
        )

        department1 = departments.get(id=form.cleaned_data.get("choice_one"))
        department2 = departments.get(id=form.cleaned_data.get("choice_two"))

        comparing_names = [
            'parameters of comparing',
            department1,
            department2
        ]

        if form.cleaned_data.get("number_staff"):
            context["number_staff"] = [
                'number staff',
                department1.staff_amount,
                department2.staff_amount,
            ]
        if form.cleaned_data.get("sum_prices_of_sold_items"):
            context["sum_prices_of_sold_items"] = [
                'sum prices of sold items',
                department1.sum_sold,
                department2.sum_sold,
            ]
        if form.cleaned_data.get("sum_prices_of_unsold_items"):
            context["sum_prices_of_unsold_items"] = [
                'sum prices of unsold items',
                department1.sum_unsold,
                department2.sum_unsold,
            ]
        if form.cleaned_data.get("sum_prices_of__all_items"):
            context["sum_prices_of_all_items"] = [
                'sum prices of all items',
                department1.sum,
                department2.sum,
            ]
        if form.cleaned_data.get("number_prices_of_sold_items"):
            context["number_prices_of_sold_items"] = [
                'number prices of sold items',
                department1.number_sold,
                department2.number_sold,
            ]
        if form.cleaned_data.get("number_prices_of_unsold_items"):
            context["number_prices_of_unsold_items"] = [
                'number prices of unsold items',
                department1.number_unsold,
                department2.number_unsold,
            ]
        if form.cleaned_data.get("number_prices_of_all_items"):
            context["number_prices_of_sold_all_items"] = [
                'number prices of all items',
                department1.number,
                department2.number,
            ]

        return render(self.request, "task1/compare_view.html",
                      context={'data': context, 'comparing_names': comparing_names})


class ItemsNotSoldView(TemplateView):

    template_name = 'task1/items_not_sold.html'
