from django.shortcuts import render

# Create your views here.
from orders.models import EnvioMethod, PaymentMethod
from orders.forms import OrderForm


from django.http import JsonResponse
from django.template.loader import render_to_string



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape

from orders.forms import OrderForm




def get_form_errors(form_errors):
    # Procesar errores de manera legible
    errors = []
    for field, messages in form_errors:
        for message in messages:
            # Si el error no pertenece a un campo específico
            if field == '__all__':
                errors.append(escape(message))
            else:
                errors.append(f"{field.capitalize()}: {escape(message)}")
    
    # Juntar los errores en un solo string separado por |
    error_message = " | ".join(errors)  
    return error_message


# Desactiva la verificación CSRF solo si estás manejando solicitudes AJAX y no puedes usar el token
@csrf_exempt
def valid_form_order(request):
    
    if request.method == 'POST':
        # Recuperar los datos enviados
        id_payment = request.POST.get('payment_id')
        envio_method_id = request.POST.get('envio_method_id')

        # Procesar los datos del formulario
        form = OrderForm(request.POST)
        
        if form.is_valid():
            # Procesar la información del formulario y los datos adicionales
            name = form.cleaned_data.get('name')
            last_name = form.cleaned_data.get('last_name')
            cellphone = form.cleaned_data.get('cellphone')
            email = form.cleaned_data.get('email')
            dni = form.cleaned_data.get('dni')
            detail_order = form.cleaned_data.get('detail_order')
            
            # Manejar otros campos según el método de envío
            if envio_method_id == '1':  # Retiro en local
                name_retiro = form.cleaned_data.get('name_retiro')
                dni_retiro = form.cleaned_data.get('dni_retiro')
                
            # Envío a domicilio
            else:  
                province = form.cleaned_data.get('province')
                city = form.cleaned_data.get('city')
                address = form.cleaned_data.get('address')
                postal_code = form.cleaned_data.get('postal_code')
                detail = form.cleaned_data.get('detail')
            
            
            # Si no se pudo autenticar, agregar errores específicos
            form.add_error('password', 'La contraseña no es válida.')

        # Procesar errores del formulario
        error_message = get_form_errors(form.errors.items())
        return JsonResponse({'success': False, 'error': error_message}, status=400)



    # Manejar solicitudes no POST
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)



def extra_form_ajax(request):
    envioId = request.GET.get('envioId', '0')
    
    flag = True if envioId == '1' else False
    form = OrderForm()
    
    context = {
        'flag': flag,
        'form': form,
    }
    
    html = render_to_string('orders/extra_form.html', context)
        
    return JsonResponse({
        'html': html
    })


def order(request):
    envios_methods = EnvioMethod.objects.all()
    payment_methods = PaymentMethod.objects.all()
    form = OrderForm()
    
    context = {
        'envios_methods': envios_methods,
        'payment_methods': payment_methods,
        'form': form,
    }
    
    return render(request, "orders/order_page.html", context)
