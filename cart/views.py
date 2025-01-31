

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from cart.carrito import Carrito
from cart.utils import get_render_htmls
from products.models import Product


def some_url(request):
    return JsonResponse({"data": "hola mundoo"})


def add_product(request):
    if request.method == 'POST':
        # recupera valores de la solicitud fetch en widget_carrito.js
        producto_id = request.POST.get('productId')
        value_qty = request.POST.get('quantity', '1')
        cart_view = request.POST.get('cartView', '').lower() in ['true', '1'] # Get True or False

        if not value_qty.isdigit():    # stupid check
            message = f"Ingrese un numero entero valido..."
            return JsonResponse( {'flag_custom': False, 'message': message, 'color': 'red'} )

        # consultamos primero el producto para cancelar todo si no existiera
        product = get_object_or_404(Product, id=producto_id)

        # Recuperar carrito de la sesión del usuario
        carrito = Carrito(request)
        
        # Este metodo compara el stock con el value_add en la db, return True or False
        flag = carrito.add_product(product=product, qty= int(value_qty))
        if not flag:
            message = 'Producto Sin Stock.'
            return JsonResponse({'flag_custom':flag, 'message':message, 'color':'red'})
            
        # Esta función nos devuelve los html renderizados para insertar con AJAX
        widget_html, cart_view_html = get_render_htmls(carrito, cart_view)
        
        return JsonResponse({
            # This is for a alerts interactions with the user
            'flag_custom': flag,
            'color': 'green',
            'message': 'Producto agregado.',
            
            # This is for update some components with ajax
            'total': carrito.total_price, 
            'qty_total': carrito.total_items,
            'widget_html': widget_html,
            'cart_view_html': cart_view_html
        })
        
    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def subtract_product(request):
    if request.method == 'POST':
        producto_id = request.POST.get('productId')
        value_qty = request.POST.get('quantity', '1')
        cart_view = request.POST.get('cartView', '').lower() in ['true', '1'] # Get True or False

        # Verificamos que el value qty sea un valor numerico
        if not value_qty.isdigit():    # stupid check
            message = f"Ingrese un numero entero valido..."
            return JsonResponse({'flag_custom': False, 'message': message, 'color': 'red'})
        
        # consultamos primero el producto para cancelar todo si no existiera
        product = get_object_or_404(Product, id=producto_id)
        
        # Recuperar carrito de la sesión del usuario
        carrito = Carrito(request)
        
        # Consultamos si por algun motivo no existiera el product-id en el carrito
        if producto_id not in carrito.carrito:    # stupid check
            message = f"No esta el producto en el carrito.."
            return JsonResponse( {'flag_custom': False, 'message': message, 'color': 'red'} )

        # Este metodo restara productos del carrito si se elimina del carrito
        # retorno un delete referenciando que se quito totalmente el producto
        delete_item = carrito.subtract_product(product=product, qty= int(value_qty))
        message = "Producto eliminado del carrito." if delete_item else "Producto reducido del carrito"
        
        # Esta función nos devuelve los html renderizados para insertar con AJAX
        widget_html, cart_view_html = get_render_htmls(carrito, cart_view)
        
        return JsonResponse({
            # This is for a alerts interactions with the user
            'flag_custom': True,
            'color': 'red',
            'message': message,
            
            # This is for update some components with ajax
            'total': carrito.total_price, 
            'qty_total': carrito.total_items,
            'widget_html': widget_html,
            'cart_view_html': cart_view_html
        })
        
    return JsonResponse({'error': 'Solicitud inválida'}, status=400)
        
        
def remove_product(request):
    if request.method == 'POST':
        producto_id = request.POST.get('productId')
        cart_view = request.POST.get('cartView', '').lower() in ['true', '1'] # Get True or False

        # consultamos primero el producto para cancelar todo si no existiera
        product = get_object_or_404(Product, id=producto_id)
        
        # Recuperar el objeto que contiene al carrito de la sesión del usuario
        carrito = Carrito(request)
        
        # Consultamos si por algun motivo no existiera el product-id en el carrito
        if producto_id not in carrito.carrito:    # stupid check
            message = f"No esta el producto en el carrito.."
            return JsonResponse( {'flag_custom': False, 'message': message, 'color': 'red'} )

        # Este metodo del carrito se encarga de borrar el item del carrito de la sesion y en la db
        carrito.remove_product(product=product)

        # Esta función nos devuelve los html renderizados para insertar con AJAX
        widget_html, cart_view_html = get_render_htmls(carrito, cart_view)
        
        return JsonResponse({
            # This is for a alerts interactions with the user
            'flag_custom': True,
            'color': 'red',
            'message': 'Producto eliminado de tu carrito.',
            
            # This is for update some components with ajax
            'total': carrito.total_price, 
            'qty_total': carrito.total_items,
            'widget_html': widget_html,
            'cart_view_html': cart_view_html
        })
        
    return JsonResponse({'error': 'Solicitud inválida'}, status=400)
        

def cart_page_detail(request):
    return render(request, "cart/cart_page_detail.html")
