from django.shortcuts import render

# Create your views here.
from orders.models import EnvioMethod, PaymentMethod
from orders.forms import OrderForm


from django.http import JsonResponse
from django.template.loader import render_to_string



from django.http import JsonResponse
from orders.forms import OrderForm

from orders.utils import get_form_errors, confirm_stock_available



# Desactiva la verificación CSRF solo si estás manejando solicitudes AJAX y no puedes usar el token
# from django.views.decorators.csrf import csrf_exempt
# @ csrf_exempt
def valid_form_order(request):
    
    if request.method == 'POST':
        
        # Confirmar pedido:
        confirm_stock, error_message = confirm_stock_available(request.user.id)
        if confirm_stock is False:
            return JsonResponse({'success': False, 'error': error_message})
        
        # Recuperar los datos enviados
        id_payment = request.POST.get('payment_id')
        id_envio_method = request.POST.get('envio_method_id')

        # Procesar los datos del formulario
        form = OrderForm(request.POST, id_envio_method=id_envio_method)
        
        if form.is_valid():
            # Crear un diccionario con los datos del formulario
            order_data = {
                'name': form.cleaned_data.get('name'),
                'last_name': form.cleaned_data.get('last_name'),
                'cellphone': form.cleaned_data.get('cellphone'),
                'email': form.cleaned_data.get('email'),
                'dni': form.cleaned_data.get('dni'),
                'detail_order': form.cleaned_data.get('detail_order', ''),
                'id_payment': id_payment,
                'id_envio_method': id_envio_method,
            }
            
            # Manejar otros campos según el método de envío
             # Retiro en local
            if id_envio_method == '1': 
                order_data.update({
                    'name_retiro': form.cleaned_data.get('name_retiro'),
                    'dni_retiro': form.cleaned_data.get('dni_retiro'),
                })
            # Envío a domicilio
            else:  
                order_data.update({
                    'province': form.cleaned_data.get('province'),
                    'city': form.cleaned_data.get('city'),
                    'address': form.cleaned_data.get('address'),
                    'postal_code': form.cleaned_data.get('postal_code', ''), #no necesario
                    'detail': form.cleaned_data.get('detail', ''),
                })
            
            # Guardar los datos en la sesión
            request.session['order_data'] = order_data
            request.session.modified = True
            
            # vaya a la pagina de pago
            return JsonResponse({
                'success': True, 
                'redirect_url': '/payment_view/',
                'message': 'Pedido guardado termine su metodo de pago para finalizar'
            })
            
        # Procesar errores del formulario
        error_message = get_form_errors(form.errors.items())
        return JsonResponse({'success': False, 'error': error_message})

    # Manejar solicitudes no POST
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})



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
