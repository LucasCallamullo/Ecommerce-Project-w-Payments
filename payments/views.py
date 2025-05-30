

# Create your views here.
import mercadopago
from django.conf import settings
from django.shortcuts import render

from datetime import timedelta
from payments import utils
from payments import utils_for_mp


from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from orders.models import Order, ItemOrder

from django.utils import timezone
from django.template.defaultfilters import date

sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)


def payment_view(request, order_id):
    """
        Esta función es principalmente para permitir el pago mediante tarjetas o transferencia de forma 
        segura para el cliente a partir de la API de mercado pago
    """
    user = request.user
    if not user.is_authenticated:    # Stupids checks for problematic users
        return render(request, "payments/fail_payments.html", {"error": "Debes iniciar sesión para pagar."})

    # Optimización de consultas con select_related y prefetch_related
    order = get_object_or_404(
        Order.objects.select_related(
            'user',
            'payment',
            'shipment',
            'shipment__method',
            'status'
        ).prefetch_related(
            Prefetch('items', queryset=ItemOrder.objects.select_related('product', 'product__category'))
        ),
        id=order_id,
        user=request.user
    )
    
    if order.user != user:
        message = "Debes iniciar sesión con la cuenta que corresponda... para ver."
        return render(request, "payments/fail_payments.html", {"error": message})

    
    # obtener info de la order
    shipment_method = order.shipment.method    # get method envio associeted with the order
    payment = order.payment              # get payment from order created
    items = order.items.all()    # get items from order
    
    discount = 1    # future discount logic
    # id = 3 --> mercado pago API
    if payment.id == 3:
        preference_id, total_cart = utils_for_mp.create_preference_data(order, discount)  
    else:
        preference_id = None
        total_cart = 0
        for item in items:
            subtotal = float(item.price * item.quantity)
            total_cart += subtotal
        total_cart -= float(discount)
        total_cart += float(shipment_method.price)
        
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
        'expire_date': order.expire_at,
        'address': order.shipment.address,
        'order_email': order.email,
        'complete_name': f"{order.first_name} {order.last_name}",
        'status': order.status,
        'payment': payment,
        
        # more data info
        'total_cart': total_cart,    # this is calculated with discount and thats stuffs
    }
    
    return render(request, "payments/payments_page.html", context)


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


from django.http import JsonResponse
def crear_preferencia(request):
    cuotas = int(request.GET.get("cuotas", 1))

    # Definir el precio según la cantidad de cuotas
    precios = {1: 100, 3: 150, 6: 200}
    total_cart = precios.get(cuotas, 100)

    items = [
        {
            "title": "Producto",
            "quantity": 1,
            "currency_id": "ARS",
            "unit_price": total_cart
        }
    ]

    preference_data = {
        "items": items,
        "payment_methods": {
            "installments": cuotas
        },
        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)
    preference_id = preference_response["response"]["id"]

    return JsonResponse({"preference_id": preference_id})


def failure(request):
    
    return render(request, 'payments/failure.html')

def pending(request):
    
    return render(request, 'payments/pending.html')
