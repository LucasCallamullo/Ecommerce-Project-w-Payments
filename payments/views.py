from django.shortcuts import render

# Create your views here.
import mercadopago
from django.conf import settings
from django.http import JsonResponse

from payments.utils import confirm_order
from cart.models import Cart

from payments.utils_for_mp import generate_datetime, get_urls_ngrok
from payments.utils_for_mp import get_items_from_cart, get_items_with_discount, get_payer_info_from_form

sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)


def payment_view(request):
    """
        Esta función es principalmente para permitir el pago mediante tarjetas o transferencia de forma 
        segura para el cliente a partir de la API de mercado pago
    """
    # Generar las fechas
    expiration_date_from = generate_datetime(flag='start')
    expiration_date_to = generate_datetime(flag='end')
    
    # para ls urls ngrok -.->  ngrok http http://localhost:8000
    back_urls = get_urls_ngrok('https://generic-ecommerce-project-production.up.railway.app')
    
    # a modo de prueba usaremos algun carrito de algun usuario
    # if request.user.is_authenticated: 
        # items = get_item_from_cart(user_id=request.user.id)
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

    payment_response = sdk.payment().get(payment_id)
    payment = payment_response["response"]

    # Accede a la lista de ítems (productos) que fueron comprados
    items = payment.get("additional_info", {}).get("items", [])  # Verifica si los ítems están dentro de "additional_info"
    
    # para confirmar la orden marcarla como compra realizada
    payer = payment.get("payer", {})
    
    order = confirm_order(request, payer)
    
    cart = Cart.request.user.carrito
    
    contexto = {
        'items': items,
        'order': order,
        'payment': payment,
    }
    


    return render(request, 'payments/success.html', contexto)


def failure(request):
    
    return render(request, 'payments/failure.html')

def pending(request):
    
    return render(request, 'payments/pending.html')
