from django import template
from decimal import Decimal


register = template.Library()


@register.filter
def multiplie(first_value, second_value):
    return first_value * second_value


@register.filter
def dollars_to_euros(value):
    return str(round(Decimal(0.89) * value, 2))
