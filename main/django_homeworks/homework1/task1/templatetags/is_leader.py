from django import template
from .get_leader import get_leader


register = template.Library()


@register.simple_tag
def is_leader(department1, department2, field, order):
    leader = get_leader(department1, department2, field)
    if type(leader)\
            is not str:
        if leader == department1:
            return "leader"
