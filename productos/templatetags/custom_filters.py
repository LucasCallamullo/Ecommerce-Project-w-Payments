

from django import template

register = template.Library()

@register.filter
def intdot(value):
    """
        Formatea números con un punto como separador de miles.
    """
    try:
        value = float(value)
        return f"{value:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return value
