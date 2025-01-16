from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


from users.forms import CreateUserForm, WidgetLoginForm, EditUserForm

# This is for edit form
from django.http import JsonResponse

from django.utils.html import escape
from django.urls import reverse


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


@login_required
def close_session(request):
    logout(request)
    return redirect('Home')


def register_widget(request):
    if request.method == 'POST':
        form = WidgetLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': 'Home'})
            
            # Si no se pudo autenticar, agregar errores específicos
            form.add_error('password', 'La contraseña no es válida.')

        # Procesar errores del formulario
        error_message = get_form_errors(form.errors.items())
        return JsonResponse({'success': False, 'error': error_message})

    # Manejar solicitudes no POST
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})



def register_user(request):
    
    if request.method == 'POST':
        # recuperar los datos del formulario
        form = CreateUserForm(request.POST)
        
        # si el formulario es valido se logeara, sino con el ajax devolvera los errores
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            
            if user:
                # capaz pensar otra logica en este caso
                login(request, user)
                return JsonResponse({'success': True})
            
            else:
                # Error al autenticar por si sucediera ya que casi nunca paso
                message = 'Email o contraseña inválidos.'
                return JsonResponse({'success': False, 'error': message})  
        else:
            error_message = get_form_errors(form.errors.items())
            return JsonResponse({'success': False, 'error': error_message})
    
    # contexto necesario para cargar la pagina al ingresar
    else:
        form = CreateUserForm()

    return render(request, 'users/register_user.html', {'form': form})



