

from orders.models import Order, OrderStatus, OrderItem
from orders.models import Envio, EnvioMethod, PaymentMethod
from orders.models import Factura
from cart.models import Cart


from django.db import transaction


def confirm_order(request, payer):
    """
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
    
    order_data = request.session.get("order_data", {})
    # if not order_data:
    #    return

    try:
        with transaction.atomic():
            # Crear envío
            envio_method_id = int(order_data["id_envio_method"])
            envio_method = EnvioMethod.objects.get(id=envio_method_id)
            envio = Envio.objects.create(
                method=envio_method,
                buyer_name = order_data.get("name_retiro", ""),
                buyer_dni = order_data.get("dni_retiro", ""),
                address = order_data.get("address", ""),
                province = order_data.get("province", ""),
                city = order_data.get("city", ""),
                postal_code = order_data.get("postal_code", ""),
                detail = order_data.get("detail", ""),
            )

            # Crear factura
            mp_name = mp_last_name = mp_dni = None
            if payer:
                mp_name = payer.get("first_name", "")
                mp_last_name = payer.get("last_name", "") 
                mp_dni = payer.get("identification", {}).get("number", "")
            
            
            cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
            total_cart = sum(float(item.product.price) * item.quantity for item in cart.items.all())
            factura = Factura.objects.create(
                tipo="B",
                buyer_name=order_data["name"],
                buyer_last_name=order_data["last_name"],
                buyer_dni=order_data["dni"],
                email=order_data["email"],
                cellphone=order_data["cellphone"],
                total_items=total_cart,
                shipment_cost=envio_method.price,
                name_mp = mp_name,
                last_name_mp = mp_last_name,
                dni_mp = mp_dni,
            )

            # Crear orden
            payment_id = int(order_data["id_payment"])
            new_order = Order.objects.create(
                user=request.user,
                status=OrderStatus.objects.get(id=4),  # Orden completada
                payment=PaymentMethod.objects.get(id=payment_id),
                envio=envio,
                detail_order=order_data["detail_order"],
                factura=factura
            )

            # Crear OrderItems
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=new_order,
                    product=item.product,
                    quantity=item.quantity,
                    price=float(item.product.price)
                )
                
            # 
            return new_order

    except Exception as e:
        # Manejar errores y registrar logs si es necesario
        print(f"Error al confirmar la orden: {e}")
        return None