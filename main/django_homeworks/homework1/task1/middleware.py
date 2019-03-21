from django.shortcuts import redirect

from .models import Item, Statistics


class Task1Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        statistics = Statistics.objects.get_or_create(url=request.path)
        statistics[0].amount += 1
        statistics[0].save()

        if Item.objects.filter(is_sold=True).count() == 0 and not \
                request.path.startswith('/admin') and not \
                request.path.startswith('/message'):
            return redirect('item_not_sold')

        return self.get_response(request)
