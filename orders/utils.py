

from django.utils.html import escape
from django.db import transaction

from cart.models import CartItem
from products.models import Product


from orders.models import ShipmentMethod, ShipmentOrder, PaymentMethod
from orders.models import StatusOrder, Order, ItemOrder
from cart.carrito import Carrito
from django.utils import timezone
from datetime import timedelta


def create_order_pending(order_data, request):
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
        "name_retire": "lucas",
        "dni_retire": "martinez",
        
        # NOTE if id_envio_method != '1': # Home delivery
        "province": "Córdoba",
        "city": "Córdoba Capital",
        "address": "Av. Colón 1234",
        "postal_code": "5000",
        "detail": "Departamento 2B",
        
        # NOTE this is for use to complete de order
        "shipping_method_id": "2", 
        "payment_method_id": "3"
    }
    """
    
    required_fields = ['shipping_method_id', 'payment_method_id']
    if not all(field in order_data for field in required_fields):
        raise ValueError("Faltan campos requeridos en order_data")

    try:
        shipping_method = ShipmentMethod.objects.get(id=order_data['shipping_method_id'])
        payment_method = PaymentMethod.objects.get(id=order_data['payment_method_id'])
        status_order = StatusOrder.objects.get(id=2)  # Orden en estado "Pendiente"
    except (ShipmentMethod.DoesNotExist, PaymentMethod.DoesNotExist) as e:
        raise ValueError("Método de envío o pago no válido") from e
    
    # Validar carrito
    carrito = Carrito(request)
    if not carrito.items:
        raise ValueError("El carrito está vacío")

    with transaction.atomic():
        
        # Create shipping order to associate with the order
        shipment = ShipmentOrder.objects.create(
            method=shipping_method,
            name_pickup=order_data.get("name_retire", ""),
            dni_pickup=order_data.get("dni_retire", ""),
            address=order_data.get("address", ""),
            province=order_data.get("province", ""),
            city=order_data.get("city", ""),
            postal_code=order_data.get("postal_code", ""),
            detail=order_data.get("detail", ""),
        )
        
        # 1	Efectivo
        # 2	Transferencia
        # 3	Tarjeta Crédito o Debito
        # 4	USD Theter
        expire_at = timezone.now() + timedelta(hours=payment_method.time)

        # Create new Order
        new_order = Order.objects.create(
            user=request.user,
            status=status_order,
            payment=payment_method,
            shipment=shipment,
            first_name=order_data.get("first_name", ""),
            last_name=order_data.get("last_name", ""),
            email=order_data.get("email", ""),
            cellphone=order_data.get("cellphone", ""),
            dni=order_data.get("dni", ""),
            detail_order=order_data.get("detail_order", ""),
            invoice=None, # primero será null y se creara despues una vez confirmado el pago
            expire_at=expire_at
        )
        
        # Obtener todos los productos del carrito en una sola consulta
        # 3. Agregar items
        product_ids = [item["id"] for _, item in carrito.items]
        products = {p.id: p for p in Product.objects.filter(id__in=product_ids)}
        
        for _, item in carrito.items:
            product = products.get(item["id"])
            if not product:
                raise ValueError(f"Producto ID {item['id']} no encontrado")
                
            if product.stock < item["qty"]:
                raise ValueError(f"Stock insuficiente para {product.name}")
            
            ItemOrder.objects.create(
                order=new_order,
                product=product,
                quantity=item["qty"],
                price=product.price
            )
            
        return new_order, "La nueva orden fue creada con exito!"


def confirm_stock_availability(user_id):
    """
    Función optimizada para reservar stock de los productos en el carrito.
    Utiliza transacciones atómicas y bloqueo de registros para evitar condiciones de carrera.
    
    Args:
        user_id (int): ID del usuario cuyo carrito se va a procesar
    
    Returns:
        string: 
            - 'stock' si no hay suficiente stock disponible para algún producto
            - 'empty' si no hay productos en el carrito
            - 'continue' si se pudo reservar el stock para todos los productos
    
    Casos de uso cubiertos:
        1. Carrito con múltiples productos
        2. Carrito con un solo producto
        3. Carrito vacío (devuelve True)
        4. Productos sin suficiente stock (devuelve False)
        5. Acceso concurrente al mismo producto (manejado con select_for_update)
    """
    with transaction.atomic():  # Inicia una transacción atómica
        # CASO 1: Obtener items del carrito con sus productos en una sola consulta
        # Esto cubre los casos de carritos con uno o múltiples productos
        cart_items = CartItem.objects.filter(
            cart__user_id=user_id  # Filtra por el usuario
        ).select_related(  # Hace JOIN con Product para evitar consultas adicionales
            'product'
        ).only(  # Selecciona solo los campos necesarios para optimizar
            'quantity', 'product__id'
        )
        
        # CASO 2: Carrito vacío
        # Si no hay items, la función termina aquí y devuelve False
        if not cart_items.exists():
            return 'empty'
        
        # CASO 3: Bloqueo concurrente de productos
        # Obtenemos y bloqueamos todos los productos necesarios en una sola consulta
        # Esto previene condiciones de carrera en operaciones concurrentes
        product_ids = [item.product_id for item in cart_items]  # Lista de IDs
        products = Product.objects.filter(
            id__in=product_ids  # Filtra por los IDs de productos en el carrito
        ).select_for_update(     # Bloquea los registros para escritura
        ).in_bulk()  # Devuelve un diccionario {id: product} para acceso rápido
        
        # CASO 4: Procesamiento de cada item del carrito
        for item in cart_items:
            product = products.get(item.product_id)  # Acceso O(1) al producto
            
            # CASO 4.1: Producto no encontrado (improbable pero posible)
            if product is None:
                return 'stock'
                
            # CASO 4.2: Intento de reserva de stock
            if not product.make_stock_reserved(item.quantity):
                # Si falla la reserva, la transacción se revierte automáticamente
                return 'stock'
                
    # CASO 5: Éxito - todos los productos tuvieron suficiente stock
    return 'continue'
