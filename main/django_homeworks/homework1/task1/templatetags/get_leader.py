from django import template
from ..models import Department


register = template.Library()


@register.simple_tag
def get_leader(department1: 'Department', department2: 'Department', field):

    department_leader = None

    if field == 'number staff':
        department_leader = department1 if department1.staff_amount > department2.staff_amount \
            else department2 if department1.staff_amount != department2.staff_amount else "equal"
    if field == 'sum prices of sold items':
        if department1.sum_sold is None and department2.sum_sold is None:
            department_leader = 'equal'
        elif department1.sum_sold is None:
            department_leader = department2
        elif department2.sum_sold is None:
            department_leader = department1
        else:
            department_leader = department1 if department1.sum_sold > department2.sum_sold  \
                else department2 if department1.sum_sold != department2.sum_sold else "equal"
    if field == 'sum prices of unsold items':
        if department1.sum_sold is None and department2.sum_sold is None:
            department_leader = 'equal'
        elif department1.sum_sold is None:
            department_leader = department2
        elif department2.sum_sold is None:
            department_leader = department1
        else:
            department_leader = department1 if department1.sum_unsold > department2.sum_unsold \
                else department2 if department1.sum_unsold != department2.sum_unsold else "equal"
    if field == 'sum prices of all items':
        if department1.sum_sold is None and department2.sum_sold is None:
            department_leader = 'equal'
        elif department1.sum_sold is None:
            department_leader = department2
        elif department2.sum_sold is None:
            department_leader = department1
        else:
            department_leader = department1 if department1.sum > department2.sum  \
                else department2 if department1.sum != department2.sum else "equal"
    if field == 'number prices of sold items':
        if department1.sum_sold is None and department2.sum_sold is None:
            department_leader = 'equal'
        elif department1.sum_sold is None:
            department_leader = department2
        elif department2.sum_sold is None:
            department_leader = department1
        else:
            department_leader = department1 if department1.number_sold > department2.number_sold  \
                else department2 if department1.number_sold != department2.number_sold else "equal"
    if field == 'number prices of unsold items':
        if department1.sum_sold is None and department2.sum_sold is None:
            department_leader = 'equal'
        elif department1.sum_sold is None:
            department_leader = department2
        elif department2.sum_sold is None:
            department_leader = department1
        else:
            department_leader = department1 if department1.number_unsold > department2.number_unsold \
                else department2 if department1.number_unsold != department2.number_unsold else "equal"
    if field == 'number prices of all items':
        if department1.sum_sold is None and department2.sum_sold is None:
            department_leader = 'equal'
        elif department1.sum_sold is None:
            department_leader = department2
        elif department2.sum_sold is None:
            department_leader = department1
        else:
            department_leader = department1 if department1.number > department2.number  \
                else department2 if department1.number != department2.number else "equal"

    return department_leader
