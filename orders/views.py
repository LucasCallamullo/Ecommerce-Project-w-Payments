from django.shortcuts import render

# Create your views here.
from orders.models import ShipmentMethod, PaymentOrder

from django.http import JsonResponse
from django.template.loader import render_to_string


def order(request):
    """ 
        Esta vista se llama para ver el formulario (se valida con serializers), ver opciones
        de metodos de pago y envío, y actuar en consecuencia segun el metodo de pago y envío.
    """
    if not request.user.is_authenticated:
        context = {'flag_to_login': True}
        return render(request, "users/register_user.html", context)
        
    # Obtenemos los distintos envios y metodos de pago para actualizar dinamicamente
    envios_methods = ShipmentMethod.objects.all()
    payment_methods = PaymentOrder.objects.all()
    
    context = {
        'envios_methods': envios_methods,
        'payment_methods': payment_methods
    }
    
    return render(request, "orders/order_page.html", context)


def extra_form_ajax(request):
    """
        Esta vista nos permite agregar un formulario extra dinamicamente a nuestra vista segun el metodo
        de envio que elija el usuario.
    """
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
    
    envioId = request.GET.get('envioId', '0')
    flag = True if envioId == '1' else False
    
    context = {
        'flag': flag,
        'provinces': PROVINCIAS_CHOICES
    }
    # renderizamos desde el servidor el extra form a agregar 
    html_extra_form = render_to_string('orders/extra_form.html', context)
        
    return JsonResponse({'html': html_extra_form})

