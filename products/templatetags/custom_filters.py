

from django import template
from django.utils.html import escapejs
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter
def escape_data(value):
    """Escapa para atributos data-* y Unicode."""
    value = str(value)
    value = escapejs(value)
    value = (
        value.replace('"', '&quot;')
             .replace("'", '&#39;')
             .replace('\u2028', '\\u2028')
             .replace('\u2029', '\\u2029')
    )
    return mark_safe(value)


@register.filter
def intdot(value):
    """
        Formatea números con un punto como separador de miles.
    """
    try:
        value = float(value)
        
        if value == 0:
            return f"0"
        
        return f"{value:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return value


@register.filter
def multiply(value, arg):
    """
    Multiplica dos valores.
    :param value: El primer valor (precio).
    :param arg: El segundo valor (cantidad).
    :return: El resultado de la multiplicación.
    """
    try:
        value = float(value) * int(arg)
        return f"{value:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return 0