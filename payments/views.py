

# Create your views here.
import mercadopago
from django.conf import settings
from django.shortcuts import render

from datetime import timedelta
from payments import utils
from payments import utils_for_mp
from orders.models import Order

sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)


def payment_view(request):
    """
        Esta función es principalmente para permitir el pago mediante tarjetas o transferencia de forma 
        segura para el cliente a partir de la API de mercado pago
    """
    user = request.user
    if not user.is_authenticated:    # Stupids checks for problematic users
        return render(request, "payments/fail_payments.html", {"error": "Debes iniciar sesión para pagar."})

    # Generar las fechas
    expiration_date_from = utils_for_mp.generate_datetime(flag='start')
    expiration_date_to = utils_for_mp.generate_datetime(flag='end', hours_window=1)
    
    # get urls for mp payments
    back_urls = utils_for_mp.get_urls_ngrok(settings.BASE_URL_RAILWAY)
    
    # Obtener lista de items que nos solicita
    # Al usar check out pro incluiremos al costo de envio si existiera como un item
    items, total_cart = utils_for_mp.get_items_from_cart(request)
    discount = 0    # Aplicar descuento en caso de que exista cuando se habilite el modelo de cupones
    if discount > 0:
        items, total_cart = utils_for_mp.get_items_with_discount(items, discount, total_cart)
    
    # obtener el diccionario con info del comprador
    payer = utils_for_mp.get_payer_info_from_form(request)
    
    # Create order and factura asociados a esta venta
    order, message = utils.create_order_pending(request)
    if order is None:    # for some reason..
        return render(request, "payments/fail_payments.html", {"error": message})    
    
    # Diccionario corregido
    preference_data = {
        "items": items,  
        "payer": payer,
        "back_urls": back_urls,
        "auto_return": "approved",    # vuelve al back_url que corresponda en 5 segundos o con el btn
        "payment_methods": {
            "excluded_payment_methods" : [
                { "id" : "argencard" },
                { "id" : "cmr" },
                { "id" : "diners" },
                { "id" : "tarshop" }
            ],
            "excluded_payment_types" : [],
            "installments" : 3
        },
        "notification_url": "https://www.your-site.com/ipn",
        "statement_descriptor": "MEUNEGOCIO",
        "external_reference": "Reference_1234",
        # fechas calculadas con la fucnion en payments/utils.py
        "expires": True, 
        "expiration_date_from": expiration_date_from,
        "expiration_date_to": expiration_date_to,
        # agregados
        "binary_mode": True, # para tener dos estados pagado o fail
        # "purpose": "wallet_purchase", # para solo permitir que paguen usuarios registrados
        
        # Referencia externa asociada con la orden
        "external_reference": str(order.id),  
    }

    # Crea la preferencia en Mercado Pago
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    
    # Obtiene el ID de la preferencia que se pasa como contexto
    preference_id = preference["id"]
    
    # obtener info de la order
    items = order.items.all()      # get Orderitems associeted with the order    
    shipment_method = order.shipment.method    # get method envio associeted with the order
    payment = order.payment              # get payment from order created
    
    # get date and hours in Argentina
    date = (order.created_at - timedelta(hours=3)).strftime("%d/%m/%Y")
    hour = (order.created_at - timedelta(hours=3)).strftime("%H:%M")

    context = {
        'preference_id': preference_id,    # esto es para crear el brick en el front asociado al monto
        'public_key': settings.MERCADO_PAGO_PUBLIC_KEY,    # mandamos nuestra clave publica al front
        
        # order stuff
        'items': items,        
        'shipment_method': shipment_method,    
        'discount': discount,
        
        'date': date,
        'hour': hour,
        'payment': payment,
        
        # more data info
        'total_cart': total_cart,    # this is calculated with discount and thats stuffs
        'payer': payer
    }
    
    return render(request, "payments/payments.html", context)


    # merchant_order_id = request.GET.get("merchant_order_id")
    # payment_id = request.GET.get("payment_id")
    # status = request.GET.get("status")  # 'approved', 'rejected', 'pending', etc.
def success(request):
    
    # Recupera el ID del pago que Mercado Pago envió en la notificación
    payment_id = int(request.GET.get('payment_id'))

    # Recuperamos los datos del payment despues del success por mercado pago para almacenar informacion
    payment_response = sdk.payment().get(payment_id)
    payment_mp = payment_response["response"]
    
    # Obtén el `external_reference` (que es el ID de la orden)
    external_reference = payment_mp.get("external_reference")
    
    # Si `external_reference` existe, puedes asociarlo con la orden de tu sistema
    order = Order.objects.get(id=external_reference)  # Aquí asocias el pago con tu orden
    message_error = "Salio todo bien"    # for debug
    if not order:    # stupid check
        message_error = "No hubo external reference o no se asocio bien el id"

    # get the order and factura created
    invoice, message = utils.confirm_order(request, payment_mp, order)
    
    # Asignar el número de factura basado en el ID generado
    if invoice:    # stupid check
        invoice.invoice_number = f"FAC-{invoice.id:06d}"
        invoice.save()
    
    
    items = order.items.all()      # get Orderitems associeted with the order    
    shipment = order.shipment
    shipment_method = order.shipment.method    # get method envio associeted with the order
    payment = order.payment              # get payment from order created
    
    
    contexto = {
        'order': order,
        'invoice': invoice,
        'items': items,
        'shipment': shipment,    # no se usa en template
        'shipment_method': shipment_method,
        'payment': payment,
        
        # this is for debug
        'message': message,
        'message_error': message_error,
        
        'payment_mp': payment_mp
    }
    


    return render(request, 'payments/success.html', contexto)




"""
def payment_view(request):
    ""
        Esta función es principalmente para permitir el pago mediante tarjetas o transferencia de forma 
        segura para el cliente a partir de la API de mercado pago
    ""
    user = request.user
    
    if not user.is_authenticated:    # Checks for some reason you know about that 
        return render(request, "login.html", {"error": "Debes iniciar sesión para pagar."})

    # Generar las fechas
    expiration_date_from = generate_datetime(flag='start')
    expiration_date_to = generate_datetime(flag='end')
    
    # get urls for mp payments
    back_urls = get_urls_ngrok(settings.BASE_URL_RAILWAY)
    
    # a modo de prueba usaremos algun carrito de algun usuario
    items, total_cart = get_items_from_cart(request)
    
    # Aplicar descuento en caso de que exista cuando se habilite el modelo de cupones
    discount = 0
    if discount > 0:
        items, total_cart = get_items_with_discount(items, discount, total_cart)
    
    # obtener el diccionario con info del comprador
    payer = get_payer_info_from_form(request)
    
    # Diccionario corregido
    preference_data = {
        "coupon_amount":  10, # verificar despues como usar en el brick
        "items": items,  
        "payer": payer,
        "back_urls": back_urls,
        "auto_return": "approved",    # vuelve al back_url que corresponda en 5 segundos o con el btn
        "payment_methods": {
            "excluded_payment_methods" : [
                { "id" : "argencard" },
                { "id" : "cmr" },
                { "id" : "diners" },
                { "id" : "tarshop" }
            ],
            "excluded_payment_types" : [],
            "installments" : 1
        },
        "notification_url": "https://www.your-site.com/ipn",
        "statement_descriptor": "MEUNEGOCIO",
        "external_reference": "Reference_1234",
        # fechas calculadas con la fucnion en payments/utils.py
        "expires": True, 
        "expiration_date_from": expiration_date_from,
        "expiration_date_to": expiration_date_to,
        # agregados
        "binary_mode": True, # para tener dos estados pagado o fail
        # "purpose": "wallet_purchase", # para solo permitir que paguen usuarios registrados
    }

    # Crea la preferencia en Mercado Pago
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    
    # Obtiene el ID de la preferencia que se pasa como contexto
    preference_id = preference["id"]
    
    context = {
        'preference_id': preference_id,
        'public_key': settings.MERCADO_PAGO_PUBLIC_KEY,
        'payer': payer
    }
    
    return render(request, "payments/payments.html", context)



def success(request):
    # Recupera el ID del pago que Mercado Pago envió en la notificación
    payment_id = int(request.GET.get('payment_id'))

    # Recuperamos los datos del payment despues del success por mercado pago para almacenar informacion
    payment_response = sdk.payment().get(payment_id)
    payment = payment_response["response"]

    # Verifica si los ítems están dentro de "additional_info"
    items = payment.get("additional_info", {}).get("items", [])
    
    # para confirmar la orden marcarla como compra realizada
    payer = payment.get("payer", {})
    
    # get the order and factura created
    order, factura, message = confirm_order(request, payer)
    
    # Asignar el número de factura basado en el ID generado
    if factura:    # stupid check
        factura.invoice_number = f"FAC-{factura.id:06d}"
        factura.save()
    
    cart = request.user.carrito
    
    contexto = {
        'cart': cart,
        'order': order,
        
        # this is for debug
        'message': message,
        
        'items': items,
        'payer': payer,
        'payment': payment,
    }
    


    return render(request, 'payments/success.html', contexto)

"""






def failure(request):
    
    return render(request, 'payments/failure.html')

def pending(request):
    
    return render(request, 'payments/pending.html')
