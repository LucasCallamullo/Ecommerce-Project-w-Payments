

# Create your views here.
from django.shortcuts import render
from products.models import Product

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
    
    products = Product.objects.all()
    products = products.filter(category=1)

    context = { 'products': products }
    
    if tab_name == 'first-tab':
        html_content = render_to_string('users/tabs/pedidos.html', context)
        scripts = None
        # scripts = ['/static/js/pedidos.js']  # Ruta al script
        return JsonResponse({'html': html_content, 'scripts': scripts})

    if tab_name == 'second-tab':
        html_content = render_to_string('users/tabs/favoritos.html', context)
        scripts = ['/static/users/js/favoritos.js']
        return JsonResponse({'html': html_content, 'scripts': scripts})

    if tab_name == 'third-tab':
        html_content = render_to_string('users/tabs/compras.html', context)
        scripts = ['/static/js/compras.js']
        return JsonResponse({'html': html_content, 'scripts': scripts})


    return JsonResponse({'error': 'Tab not found'}, status=404)






