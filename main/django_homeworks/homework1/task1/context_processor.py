from .models import Item


def processor(request):
    return {'ITEMS_AMOUNT': Item.objects.filter(is_sold=False).count()}
