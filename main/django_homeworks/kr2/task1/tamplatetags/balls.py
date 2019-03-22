from django import template
from ..models import Department


register = template.Library()


@register.simple_tag
def balls(value):

    result = None

    if 0 < value < 5:
        result = f'{value} баллов'
    elif value == 1:
        result = f'{value} балл'
    else:
        result = f'{value} балла'

    return result
