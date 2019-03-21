from django import template
from ..models import Department


register = template.Library()


@register.simple_tag
def get_leader(department1: 'Department', department2: 'Department', field):

    department_leader = None

    print(department1, department2, field)

    if field == 'number staff':
        department_leader = department1 if department1.staff_amount > department2.staff_amount else department2
    if field == 'sum prices of sold items':
        department_leader = department1 if department1.sum_sold > department2.sum_sold else department2
    if field == 'sum prices of unsold items':
        department_leader = department1 if department1.sum_unsold > department2.sum_unsold else department2
    if field == 'sum prices of all items':
        department_leader = department1 if department1.sum > department2.sum else department2
    if field == 'number prices of sold items':
        department_leader = department1 if department1.number_sold > department2.number_sold else department2
    if field == 'number prices of unsold items':
        department_leader = department1 if department1.number_unsold > department2.number_unsold else department2
    if field == 'number prices of all items':
        department_leader = department1 if department1.number > department2.number else department2

    return department_leader
