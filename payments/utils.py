

from orders.models import Order, StatusOrder, ItemOrder, InvoiceOrder
from orders.models import ShipmentMethod, ShipmentOrder, PaymentOrder

from cart.carrito import Carrito
from products.models import Product
from django.utils import timezone
from datetime import timedelta

from django.db import transaction

def create_order_pending(request):
    """
    esta funcion nos sirve para almacenar y guardar todos los datos en la base de datos y asociarlo
    segun corresponda con cada base de datos
    
    # example on order data
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
    # recuperamos el order data de la session en el paso anterior que se guardo
    order_data = request.session.get("order_data", {})
    if not order_data:    # stupid check
        return None, "Por algun motivo.. No hay datos de orden disponibles."

    try:
        with transaction.atomic():
            envio_method_id = int(order_data.get("envio_method_id", 0))
            payment_id = int(order_data.get("payment_method_id", 0))

            if not envio_method_id or not payment_id:    # stupid check
                return None, "Por algun motivo.. Falta el método de envío o pago."

            # Crear envío
            shipment_method = ShipmentMethod.objects.get(id=envio_method_id)
            shipment = ShipmentOrder.objects.create(
                method=shipment_method,
                name_pickup=order_data.get("name_retiro", ""),
                dni_pickup=order_data.get("dni_retiro", ""),
                address=order_data.get("address", ""),
                province=order_data.get("province", ""),
                city=order_data.get("city", ""),
                postal_code=order_data.get("postal_code", ""),
                detail=order_data.get("detail", ""),
            )

            # Crear orden
            payment_method = PaymentOrder.objects.get(id=payment_id)
            status = StatusOrder.objects.get(id=2)  # Orden en estado "Pendiente"
            user = request.user
            expire_at = timezone.now() + timedelta(hours=1)

            new_order = Order.objects.create(
                user=user,
                status=status,
                payment=payment_method,
                shipment=shipment,
                detail_order=order_data.get("detail_order", ""),
                invoice=None,    # primero será null y se creara despues una vez confirmado el pago
                expire_at=expire_at
            )
            
            # Obtenemos el carrito de la session
            carrito = Carrito(request)
            
            # Obtener todos los productos del carrito en una sola consulta
            product_ids = [value["id"] for _, value in carrito.items]
            products = {product.id: product for product in Product.objects.filter(id__in=product_ids)}
            
            for _, value in carrito.items:
                
                 # Acceder al producto ya consultado
                product = products.get(value["id"]) 

                ItemOrder.objects.create(
                    order=new_order,
                    product=product,
                    quantity=value["qty"],
                    price=product.price
                )
        
            return new_order, "La nueva orden fue creada con exito!"
        
    except Exception as e:
        return None, f"Error al confirmar la orden: {e}"


def confirm_order(request, payment_mp, order):
    """
    esta funcion nos sirve para almacenar y guardar todos los datos en la base de datos y asociarlo
    segun corresponda con cada base de datos
    
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
    # recuperamos el order data de la session en el paso anterior que se guardo
    order_data = request.session.get("order_data")
    if not order_data:    # stupid check
        return None, "No hay datos de orden disponibles."

    user = request.user    # get user
    if not user.is_authenticated:    # stupid check
        return None, "Usuario no autenticado."
    
    # Verifica si los ítems están dentro de "additional_info"
    # items_mp = payment_mp.get("additional_info", {}).get("items", [])
    
    # obtenemos los datos reales de quien pago en mercado pago
    payer = payment_mp.get("payer", {})
    
    # obtenemos el id unico de la preferencia de mp
    payment_id_mp = payment_mp.get("id", {})
    
    transaction_details = payment_mp.get("transaction_details", {})

    # 
    try:
        with transaction.atomic():
            
            # Extraer datos del payer(pagador) from MP API of the response success
            mp_name = mp_last_name = mp_dni = mp_email = None
            if payer:
                mp_name = payer.get("first_name", None)
                mp_last_name = payer.get("last_name", None)
                mp_email = payer.get("email", None)
                identification = payer.get("identification", None)
                if identification:
                    mp_dni = identification.get("number", None)

            # Obtenemos el carrito de la session
            carrito = Carrito(request)
            total_cart = carrito.total_price

            # Crear factura
            invoice = InvoiceOrder.objects.create(
                f_type="B",
                name= f"{order_data.get("first_name", "")} {order_data.get("last_name", "")}",
                dni=order_data.get("dni", ""),
                email=order_data.get("email", ""),
                cellphone=order_data.get("cellphone", ""),
                
                total=total_cart,    
                shipment_cost=order.shipment.method.price,    # get cost shipment
                total_mp=transaction_details.get("net_received_amount", None),
                
                name_mp=f"{mp_name} {mp_last_name}",
                dni_mp=mp_dni,
                email_mp=mp_email,
                invoice_number=None  # This generate after create Factura
            )

            # Crear orden
            status = StatusOrder.objects.get(id=3)  # Orden en estado "Pendiente"
            order.status = status  # Cambiar estado a "Pendiente"
            order.invoice = invoice  # Asociar factura
            order.save()  # Guardar cambios en la base de datos
            
            # Vaciar el carrito tras la compra
            carrito.clear()

            return invoice, "La nueva factura fue creada con exito!"

    except Exception as e:
        return None, f"Error al confirmar la orden: {e}"
    