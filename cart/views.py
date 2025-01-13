from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


# Create your views here.
from cart.carrito import Carrito
from productos.models import Product

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

""" 
from cart.models import Cart, ItemCart

def migrar_carrito_sesion_a_db(request):
    carrito_sesion = request.session.get("carrito", {})
    if request.user.is_authenticated:
        carrito_db, created = Cart.objects.get_or_create(usuario=request.user)
        for item_id, datos in carrito_sesion.items():
            ItemCart.objects.update_or_create(
                carrito=carrito_db,
                producto_id=item_id,
                defaults={"cantidad": datos["cantidad"]}
            )
        request.session["carrito"] = {}
"""

from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder


def update_productos(request):

    if request.method == 'POST':
        try:
            # recupera valores del widget_carrito.js
            producto_id = int(request.POST.get('producto_id'))
            action = request.POST.get('action')
            value_add = int(request.POST.get('value'))
            
            # consultamos primero el producto para cancelar todo si no existiera
            producto = get_object_or_404(Product, id=producto_id)

            # Recuperar carrito de la sesión del usuario
            if request.user.is_authenticated:
                carrito = Carrito(request)
                # carrito = Carrito.objects.filter(usuario=request.user).first()
            else:
                carrito = Carrito(request)
            
            # delegamos la accion que toma el carrito si cumple con tener stock
            flag_stock = True
            if action == 'add':
                # recuperamos la cantidad del carrito para sumarla a la nueva cantidad y consultar el stock
                flag_stock = carrito.stock_or_available(producto, value_add)
                if not flag_stock:
                    message = f'Producto Sin Stock.'
                    return JsonResponse( {'flag_stock': flag_stock, 'message': message} )
                
                carrito.add_product(producto, value_add)
                message = 'Producto agregado.'

            elif action == 'less':
                delete_item = carrito.less_producto(producto_id=producto_id)
                message = 'Producto reducido.' if not delete_item else 'Producto eliminado de tu carrito.'

            elif action == 'remove':
                carrito.remove_producto(producto_id=producto_id)
                message = 'Producto eliminado de tu carrito.'

            else:
                return JsonResponse({'error': 'Acción inválida'}, status=400)

            # renderizar el nuevo html que vamos a integrar con js al html
            html = render_to_string('cart/cart_items.html', {'carrito': carrito})
            
            return JsonResponse({
                'html': html, 
                'total': carrito.total_price, 
                'message': message,
                'flag_stock': flag_stock,
                'qty_total': carrito.total_items,
            })

        # cuando no exista el id en el carrito
        except ValueError:
            return JsonResponse({'error': 'ID de producto inválido'}, status=400)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def ver_carrito(request):

    return render(request, "carrito/ver_carrito.html")
