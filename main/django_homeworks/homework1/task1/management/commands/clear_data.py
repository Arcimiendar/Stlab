from django.core.management import BaseCommand
from task1.models import Item, Department, Shop


class Command(BaseCommand):

    help = 'cleare tables all tables'

    def handle(self, *args, **options):
        Item.objects.all().delete()
        Department.objects.all().delete()
        Shop.objects.all().delete()
