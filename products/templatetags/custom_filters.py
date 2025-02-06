

from django import template

register = template.Library()

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