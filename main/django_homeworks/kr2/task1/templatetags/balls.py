from django import template


register = template.Library()


@register.filter
def balls(value):

    result = None

    if 0 == value:
        result = f'{value} баллов'
    elif value >= 5:
        result = f'{value} баллов'
    elif value == 1:
        result = f'{value} балл'
    else:
        result = f'{value} балла'

    return result
