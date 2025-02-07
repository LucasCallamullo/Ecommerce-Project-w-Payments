

from datetime import datetime, timezone, timedelta
def generate_datetime(flag: str='start', hours_window: int=4, utc_offset: int=-3) -> str:
    """
    Genera una fecha y hora formateada en el estándar ISO 8601.
    
    Args:
        flag (str): Define si se genera la hora de inicio ('start') o fin ('end').
        hours_window (int): Cantidad de horas para la ventana de tiempo.
        utc_offset (int): Desfase horario en horas respecto a UTC. establecido para Argentina
    
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


def get_urls_ngrok(url: str) -> dict:
    """ 
        Obtiene de forma generica las urls necesarias para trabajar con mercado pago
    """
    if url.endswith('/'):
        url = url.rstrip("/")
    
    back_urls = {
        "success": url + "/success/",
        "failure": url + "/failure/",
        "pending": url + "/pending/"
    }
    
    return back_urls
    
    
from cart.models import Cart
from orders.models import ShipmentMethod

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

    # REcuperamos el cart asociado al usuario con prefetch_related para optimizar la consulta
    cart = Cart.objects.prefetch_related('items__product').get(user=user)
    
    for item in cart.items.all():
        price = float(item.product.price)
        quantity = item.quantity
        
        items.append({
            "id": item.product.id,
            "title": item.product.name,
            "quantity": quantity, 
            "unit_price": price,
            "currency_id": "ARS",  # Moneda (ajustar según sea necesario)
            "picture_url": item.product.main_image,
            "description": item.product.description if item.product.description else '',
            # "category_id": item.product.category.name,
            "category_id": "computing",
        })
        
        # aprovechamos el recorrido para calcular el total cart
        total_cart += price * quantity
         
    # obtenemos la info de la session
    order_data = request.session.get("order_data", {})
    
    # recuperamos el envio method para obtener sus datos y agregarlos a los items
    envio_method_id = int(order_data.get("envio_method_id", 0))    # falta un stupid check para el caso de 0
    envio_method = ShipmentMethod.objects.get(id=envio_method_id)
    
    # Al usar check out pro incluiremos al costo de envio si existiera como un item
    items.append({
        "id": envio_method.id,
        "title": envio_method.name,
        "quantity": 1, 
        "unit_price": float(envio_method.price),
        "currency_id": "ARS",  # Moneda (ajustar según sea necesario)
        # "picture_url": item.product.main_image,
        "description": "precio del envío",
        "category_id": "envío",
    })
    
    total_cart += float(envio_method.price)    # terminamos de acumular los valores
    
    return items, total_cart
    

def get_items_with_discount(items, discount, total):
    """  
        Esto es para obtener los items con un descuento total aplicado proporcionalmente
        si el descuento fueran 5000, descontaría a todos los items proporcionalmente 5000
    """
    
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
        "first_name": "Lucas",
        "last_name": "Martinez",
        "email": "lucas.martinez@example.com",
        "cellphone": "3515437688",
        "dni": "41224335",
        "detail_order": "Por favor, entregar antes de las 18:00.",
        
        # NOTE if id_envio_method == '1': # this is only for retire local
        "name_retiro": "lucas",
        "dni_retiro": "martinez",
        
        # NOTE if id_envio_method != '1': # Home delivery
        "province": "Córdoba",
        "city": "Córdoba Capital",
        "address": "Av. Colón 1234",
        "postal_code": "5000",
        "detail": "Departamento 2B",
        
        # NOTE this is for use to complete de order
        "envio_method_id": "2", 
        "payment_method_id": "3"
    }
    """
    # obtenemos la info de la session
    order_data = request.session.get("order_data", {})
    
    payer = {
        "name": order_data.get("first_name", ''),
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
    envio_method_id = int(order_data.get("envio_method_id", 0))
    if envio_method_id != 1:
        payer["address"] = {
            "street_name": order_data.get("address", ''),
            "street_number": 123,
            "zip_code": order_data.get("postal_code", ""),
        }
        
    return payer

    