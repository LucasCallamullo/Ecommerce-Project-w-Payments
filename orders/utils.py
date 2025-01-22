

from django.utils.html import escape
from cart.models import Cart


def get_form_errors(form_errors):
    # Procesar errores de manera legible
    errors = []
    for field, messages in form_errors:
        for message in messages:
            # Si el error no pertenece a un campo específico
            if field == '__all__':
                errors.append(escape(message))
            else:
                errors.append(f"{field.capitalize()}: {escape(message)}")
    
    # Juntar los errores en un solo string separado por |
    error_message = " | ".join(errors)  
    return error_message


def confirm_stock_available(user_id):
    """
        Funcion destinada a reservar stock de cada producto dentro del carrito
        para la creacion del link de pago
        
        si llegase a retornar false significa que no hay stock disponible
    """
    
    # Recuperamos el cart asociado al usuario con prefetch_related para optimizar la consulta
    cart = Cart.objects.prefetch_related('items__product').get(user_id=user_id)
    
    list_product_unreserved = []
    
    for item in cart.items.all():
        quantity = item.quantity
        flag = item.product.make_stock_reserved(quantity)
        
        # Devolvemos el nombre del producto que no tiene suficiente stock
        if flag is False:
            message = f"No hay suficiente stock de: {item.product.name}, solo "
            stock = item.product.stock
            message += f"quedan {stock} disponibles. " if stock != 1 else f"queda {stock} disponible. " 
            message += "Actualize su carrito."
            
            # deshacemos la reservacion de los items que modificamos
            make_unreservation_items(list_product_unreserved)
            return False, message
        
        # obtenemos una lista con los productos que fueron modificacods para eficiencia
        list_product_unreserved.append({"product":item.product, "qty":quantity})
        
    return True, ''
        
        
def make_unreservation_items(list_product_unreserved):
    for items in list_product_unreserved:
        product = items["product"]
        quantity = items["quantity"]
        product.make_stock_unreserved(quantity)
    
        
        
        