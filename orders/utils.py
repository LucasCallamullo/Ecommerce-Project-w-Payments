

from django.utils.html import escape
from cart.models import Cart
from products.models import Product


def confirm_stock_available(user_id):
    """
    Function to reserve stock for each product in the cart
    to create the payment link.
    
    If it returns False, it means there is not enough stock available.
    """
    
    # Recuperamos el cart asociado al usuario con prefetch_related para optimizar la consulta
    cart = Cart.objects.prefetch_related('items__product').get(user_id=user_id)
    
    list_product_unreserved = []
    
    for item in cart.items.all():
        quantity = item.quantity
        
        # Bloqueamos el producto con select_for_update para evitar condiciones de carrera
        product = Product.objects.select_for_update().get(id=item.product.id)
        
        # Llamamos al método del modelo Product para reservar el stock
        flag = product.make_stock_reserved(quantity)
        
        # Devolvemos el nombre del producto que no tiene suficiente stock
        if flag is False:
            # Deshacemos la reservación de los productos modificados
            make_unreservation_items(list_product_unreserved)
            return False
        
        # Agregamos los productos reservados para poder deshacer la reservación si es necesario
        list_product_unreserved.append({"product": product, "quantity": quantity})
        
    return True
        
def make_unreservation_items(list_product_unreserved):
    for items in list_product_unreserved:
        product = items["product"]
        quantity = items["quantity"]
        product.make_stock_unreserved(quantity)

    
# this is for legacy no not use more forms only serializers
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
        
        
        