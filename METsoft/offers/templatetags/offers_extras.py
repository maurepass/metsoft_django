from django import template

register = template.Library()


@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def percent(value, arg):
    try:
        return int(int(value) * 100 / int(arg))
    except (ValueError, ZeroDivisionError):
        return None
