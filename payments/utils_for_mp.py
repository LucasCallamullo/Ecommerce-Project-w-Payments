

from datetime import datetime, timezone, timedelta

def generate_datetime(flag='start', hours_window=4, utc_offset=-3):
    """
    Genera una fecha y hora formateada en el estándar ISO 8601.
    
    Args:
        flag (str): Define si se genera la hora de inicio ('start') o fin ('end').
        hours_window (int): Cantidad de horas para la ventana de tiempo.
        utc_offset (int): Desfase horario en horas respecto a UTC.
    
    Returns:
        str: Fecha y hora formateada en ISO 8601 con el offset de zona horaria.
    """
    # Obtener la fecha y hora actuales
    now = datetime.now(timezone.utc)  # Hora actual en UTC

    # Ajustar la hora a la zona horaria local
    start_time = now + timedelta(hours=utc_offset)

    # Calcular fecha de inicio o fin
    if flag == 'start':
        target_time = start_time
    elif flag == 'end':
        target_time = start_time + timedelta(hours=hours_window)
    else:
        raise ValueError("El parámetro 'flag' debe ser 'start' o 'end'.")

    # Formatear la fecha y hora
    formatted_time = target_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]  # Eliminar microsegundos adicionales
    formatted_time += f"{utc_offset:+03d}:00"  # Agregar el offset de zona horaria
    
    return formatted_time



def get_urls_ngrok(url):
    if url.endswith('/'):
        url = url.rstrip("/")
        
    back_urls = {
        "success": url + "/success/",
        "failure": url + "/failure/",
        "pending": url + "/pending/"
    }
    
    return back_urls
    
    
from cart.models import Cart
def get_items_from_cart(request):
    """
    Se espera que la funcion devuelva todos los items almacenados en el carrito del usuario con el formato
    que nos establece mercado pago
    items = [ {
        "id": "item-ID-1234",
        "title": "Producto 1",
        "quantity": 3,
        "unit_price": 100.00,
        "currency_id": "BRL",
        "picture_url": "https://www.mercadopago.com/org-img/MP3/home/logomp3.gif",
        "description": "Descrição do Item",
        "category_id": "art",
    },

    Args:
        user_id (_type_, optional): _description_. Defaults to None.
    """
    items = []
    total_cart = 0
    
    user = request.user
    
    # if not user.is_authenticated:
    #    return items, total_cart

    # REcuperamos el cart asociado al usuario con prefetch_related para optimizar la consulta
    cart = Cart.objects.prefetch_related('items__product').get(user=user)
    
    for item in cart.items.all():
        price = float(item.product.price)
        qty = item.quantity
        
        items.append({
            "id": item.product.id,
            "title": item.product.name,
            "quantity": qty, 
            "unit_price": price,
            "currency_id": "ARS",  # Moneda (ajustar según sea necesario)
            "picture_url": item.product.main_image,
            "description": item.product.description if item.product.description else '',
            "category_id": item.product.category.name,
        })
        
        # aprovechamos el recorrido para calcular el total cart
        total_cart += price * qty
         
    return items, total_cart
    

def get_items_with_discount(items, discount, total):
    
    # Recalcular precios proporcionalmente
    for item in items:
        item["unit_price"] -= (discount / total) * item["unit_price"]
        
    total_cart = sum(item["unit_price"] * item["quantity"] for item in items)
    
    return items, total_cart


def get_payer_info_from_form(request):
    """
        Funcion para recuperar los datos del payer como nos solicita mercado pago
    
    "payer": {     # ejemplo api mp
        "name": "João",
        "surname": "Silva",
        "email": "user@email.com",
        "phone": {
            "area_code": "11",
            "number": "4444-4444"
        },
        "identification": {
            "type": "CPF",
            "number": "19119119100"
        },
        "address": {
            "street_name": "Street",
            "street_number": 123,
            "zip_code": "06233200"
        }
    },
        
    order_data = {
        'name': form.cleaned_data.get('name'),
        'last_name': form.cleaned_data.get('last_name'),
        'cellphone': form.cleaned_data.get('cellphone'),
        'email': form.cleaned_data.get('email'),
        'dni': form.cleaned_data.get('dni'),
        'detail_order': form.cleaned_data.get('detail_order', ''),
        'id_payment': id_payment,
        'id_envio_method': id_envio_method,
    }
    if id_envio_method == '1': 
        order_data.update({
            'name_retiro': form.cleaned_data.get('name_retiro'),
            'dni_retiro': form.cleaned_data.get('dni_retiro'),
        })
    # Envío a domicilio
    else:  
        order_data.update({
            'province': form.cleaned_data.get('province'),
            'city': form.cleaned_data.get('city'),
            'address': form.cleaned_data.get('address'),
            'postal_code': form.cleaned_data.get('postal_code', ''), #no necesario
            'detail': form.cleaned_data.get('detail', ''),
        })
    """
    # obtenemos la info de la session
    order_data = request.session.get("order_data", {})
    
    payer = {
        "name": order_data.get("name", ''),
        "surname": order_data.get("last_name", ''),
        "email": order_data.get("email", ''),
        "phone": {
            "area_code": "351",
            "number": order_data.get("cellphone", ""),
        },
        "identification": {
            "type": "DNI",
            "number": order_data.get("dni", ""),
        },
    }
    
    # retiro a domicilio
    id_envio_method = int(order_data.get("id_envio_method", 0))
    if id_envio_method != 1:
        payer["address"] = {
            "street_name": order_data.get("address", ''),
            "street_number": 123,
            "zip_code": order_data.get("postal_code", ""),
        }
        
    return payer

    