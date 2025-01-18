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

        # recupera valores del widget_carrito.js
        producto_id = int(request.POST.get('producto_id'))
        action = request.POST.get('action')
        value_add = int(request.POST.get('value'))
        cart_view = request.POST.get('cart_view')
        
        # consultamos primero el producto para cancelar todo si no existiera
        product = get_object_or_404(Product, id=producto_id)

        # Recuperar carrito de la sesión del usuario
        carrito = Carrito(request)
        
        # inicializamos valores por defecto
        flag_stock = True
        delete_item = False
        
        # delegamos la accion que toma el carrito si cumple con tener stock
        if action == 'add':
            
            # usamos el metodo para verificar en base a los retornos si se pudo o no que hacer
            flag_stock = carrito.add_product(product=product, qty=value_add)
            if not flag_stock:
                message = 'Producto Sin Stock.'
                color = 'red'
                return JsonResponse( {'flag_stock': flag_stock, 'message': message, 'color': color} )
            else:
                message = 'Producto agregado.'

        elif action == 'less':
            delete_item = carrito.subtract_product(product=product, qty=value_add)
            message = 'Producto reducido.' if not delete_item else 'Producto eliminado del carrito.'
            
        elif action == 'remove':
            delete_item = carrito.remove_product(product=product)
            message = 'Producto eliminado de tu carrito.'

        else:
            return JsonResponse({'error': 'Acción inválida'}, status=400)
            
        # obtenemos el el background de fondo de la alerta para el json response
        color = 'green' if not delete_item else 'red'
        
        # renderizar el nuevo html del widget que vamos a integrar con js al html
        context = {'carrito': carrito}
        widget_html = render_to_string('cart/cart_items.html', context)
        
        # solo renderizar la vista del carrito en caso de que estemos en la pagina del carrito
        cart_view = True if cart_view == 'true' else False
        cart_view_html = None
        if cart_view:
            cart_view_html = render_to_string('cart/table_cart_detail.html', context)
        
        return JsonResponse({
            'widget_html': widget_html, 
            'total': carrito.total_price, 
            'message': message,
            'color': color,
            'flag_stock': flag_stock,
            'qty_total': carrito.total_items,
            'cart_view_html': cart_view_html
        })

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def cart_page_detail(request):
    return render(request, "cart/cart_page_detail.html")
