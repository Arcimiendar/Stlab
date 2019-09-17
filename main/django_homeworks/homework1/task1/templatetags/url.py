from django import template
from django.utils.html import format_html
from django.urls import reverse_lazy


register = template.Library()


@register.filter
def url(value):

    class_name = type(value).__name__.lower()
    url_result = reverse_lazy(f'{class_name}_edit', kwargs={'pk': value.id})
    return format_html(f'<a href="{url_result}">{value}</a>')
