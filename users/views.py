

# Create your views here.
from django.shortcuts import render
from products.models import Product
from favorites.models import FavoriteProduct
from orders.models import Order

def register_user(request):
    PROVINCIAS_CHOICES = [
        ('', 'Selecciona una provincia'),
        ('Buenos Aires', 'Buenos Aires'),
        ('Catamarca', 'Catamarca'),
        ('Chaco', 'Chaco'),
        ('Chubut', 'Chubut'),
        ('CABA', 'Ciudad Autónoma de Buenos Aires'),
        ('Córdoba', 'Córdoba'),
        ('Corrientes', 'Corrientes'),
        ('Entre Ríos', 'Entre Ríos'),
        ('Formosa', 'Formosa'),
        ('Jujuy', 'Jujuy'),
        ('La Pampa', 'La Pampa'),
        ('La Rioja', 'La Rioja'),
        ('Mendoza', 'Mendoza'),
        ('Misiones', 'Misiones'),
        ('Neuquén', 'Neuquén'),
        ('Río Negro', 'Río Negro'),
        ('Salta', 'Salta'),
        ('San Juan', 'San Juan'),
        ('San Luis', 'San Luis'),
        ('Santa Cruz', 'Santa Cruz'),
        ('Santa Fe', 'Santa Fe'),
        ('Santiago del Estero', 'Santiago del Estero'),
        ('Tierra del Fuego', 'Tierra del Fuego'),
        ('Tucumán', 'Tucumán')
    ]
    context = {'provinces': PROVINCIAS_CHOICES}
    return render(request, 'users/register_user.html', context)


def profile_page(request):
    user = request.user
    proucts = Product.objects.all()
    
    context = {
        'user': user,
        'proucts': proucts
    }
    return render(request, 'users/profile.html', context)


# This is for edit form
from django.http import JsonResponse
from django.template.loader import render_to_string

def profile_tab(request, tab_name):
    """ 
    cada condicion devuelve de forma asincrona mediante un fetch el html renderizado ademas de un javascript
    asociado para poder utilizar en la pagina
    """
    
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'Tab not found'}, status=404)
    
    
    if tab_name == 'first-tab':
        user = request.user
        # Trae órdenes junto con la factura en una sola consulta SQL
        
        if user.is_superuser:    # verificamos si es admin
            orders = Order.objects.all()
        else:
            orders = user.orders.select_related("invoice").all()
        
        context = { 'orders': orders }
        html_content = render_to_string('users/tabs/pedidos.html', context)
        return JsonResponse({'html': html_content})
        

    if tab_name == 'second-tab':
        favorites = user.favorites.select_related('product').all()
        context = {
            'products': [f.product for f in favorites],
            'favorite_product_ids': {f.product_id for f in favorites}
        }
        return JsonResponse({
            'html': render_to_string('users/tabs/favorites.html', context)
        })


    if tab_name == 'third-tab':
        
        context = {"none": None}
        
        html_content = render_to_string('users/tabs/compras.html', context)
        
        return JsonResponse({'html': html_content})


    return JsonResponse({'error': 'Tab not found'}, status=404)






