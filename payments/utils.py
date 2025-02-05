

from orders.models import Order, OrderStatus, OrderItem
from orders.models import Envio, EnvioMethod, PaymentMethod
from orders.models import Factura
from cart.carrito import Carrito

from products.models import Product


from django.db import transaction


def confirm_order(request, payer):
    """
    
    
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
        return None, None, "No hay datos de orden disponibles."

    user = request.user    # get user
    if not user.is_authenticated:    # stupid check
        return None, None, "Usuario no autenticado."

    try:
        with transaction.atomic():
            envio_method_id = int(order_data.get("envio_method_id", 0))
            payment_id = int(order_data.get("payment_method_id", 0))

            if not envio_method_id or not payment_id:    # stupid check
                return None, None, "Falta el método de envío o pago."

            # Crear envío
            envio_method = EnvioMethod.objects.get(id=envio_method_id)
            envio = Envio.objects.create(
                method=envio_method,
                buyer_name=order_data.get("name_retiro", ""),
                buyer_dni=order_data.get("dni_retiro", ""),
                address=order_data.get("address", ""),
                province=order_data.get("province", ""),
                city=order_data.get("city", ""),
                postal_code=order_data.get("postal_code", ""),
                detail=order_data.get("detail", ""),
            )

            # Extraer datos del payer(pagador) from MP API of the response success
            mp_name = mp_last_name = mp_dni = None
            if payer:
                mp_name = payer.get("first_name", None)
                mp_last_name = payer.get("last_name", None)
                identification = payer.get("identification", None)
                if identification:
                    mp_dni = identification.get("number", None)

            # Obtener carrito
            # cart = Cart.objects.prefetch_related('items__product').get(user=user)
            # total_cart = sum(float(item.product.price) * item.quantity for item in cart.items.all())
            
            # Obtenemos el carrito de la session
            carrito = Carrito(request)
            total_cart = carrito.total_price

            # Crear factura
            factura = Factura.objects.create(
                f_type="B",
                buyer_name=order_data.get("first_name", ""),
                buyer_last_name=order_data.get("last_name", ""),
                buyer_dni=order_data.get("dni", ""),
                email=order_data.get("email", ""),
                cellphone=order_data.get("cellphone", ""),
                total_items=total_cart,
                shipment_cost=envio_method.price,
                name_mp=mp_name,
                last_name_mp=mp_last_name,
                dni_mp=mp_dni,
                invoice_number=None  # This generate after create Factura
            )

            # Crear orden
            payment_method = PaymentMethod.objects.get(id=payment_id)
            status = OrderStatus.objects.get(id=2)  # Orden en estado "Pendiente"

            new_order = Order.objects.create(
                user=user,
                status=status,
                payment=payment_method,
                envio=envio,
                detail_order=order_data.get("detail_order", ""),
                factura=factura
            )

            # Crear OrderItems
            """  for item in cart.items.all():
                OrderItem.objects.create(
                    order=new_order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            """
            # Obtener todos los productos del carrito en una sola consulta
            product_ids = [value["id"] for _, value in carrito.items]
            products = {product.id: product for product in Product.objects.filter(id__in=product_ids)}
            
            for _, value in carrito.items:
                
                 # Acceder al producto ya consultado
                product = products.get(value["id"]) 

                OrderItem.objects.create(
                    order=new_order,
                    product=product,
                    quantity=value["qty"],
                    price=product.price
                )

            # Vaciar el carrito tras la compra
            carrito.clear()
            # cart.items.all().delete()

            return new_order, factura, "La nueva orden fue creada con exito!"

    except Exception as e:
        return None, None, f"Error al confirmar la orden: {e}"
