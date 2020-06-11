from django import template

register = template.Library()


@register.filter
def multiplie(first_value, second_value):
    return first_value * second_value
