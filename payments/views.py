from django.shortcuts import render

# Create your views here.


def payment(request):
    order_data = request.session.get('order_data', None)
    
    # Verifica los datos en la consola del servidor
    print(order_data)  # Esto te mostrará los datos en la consola

    context = {
        'order_data': order_data
    }
    
    return render(request, "payments/payments.html", context)