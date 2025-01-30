

from functools import wraps
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from users.models import CustomUser


def jwt_required(view_func):
    """
    Decorador para proteger vistas con JWT en Django sin usar DRF.
    Verifica el token en la cookie o en los headers y autentica al usuario.
    """
    @wraps(view_func)  # Esto asegura que la vista decorada mantiene su nombre y su docstring.
    def _wrapped_view(request, *args, **kwargs):
        
        # Primero, intenta obtener el token desde las cookies (preferido en este caso).
        token = request.COOKIES.get('access_token')  # Prioriza la cookie, ya que es más seguro.
        
        # Si no se encuentra el token en las cookies, intenta obtenerlo desde el header de autorización.
        if not token:
            auth_header = request.headers.get('Authorization', '')  # Obtiene el header de Authorization.
            if auth_header.startswith('Bearer '):  # Verifica si el header tiene el prefijo 'Bearer'.
                token = auth_header.split('Bearer ')[-1]  # Extrae el token del header.

        # Si no se encuentra el token ni en las cookies ni en los headers, responde con un error 401.
        if not token:
            return JsonResponse({'error': 'Unauthorized - Token missing'}, status=401)

        try:
            # Intenta validar el token usando la clase AccessToken (puede ser de alguna librería como PyJWT o similar).
            access_token = AccessToken(token)
            # Obtiene el 'user_id' del token. Este es un ejemplo de cómo se podría hacer con JWT.
            user_id = access_token.get('user_id')

            # Si no se encuentra el 'user_id' en el token, responde con un error 401.
            if not user_id:
                return JsonResponse({'error': 'Unauthorized - Invalid token'}, status=401)

            # Verifica si el usuario existe en la base de datos usando el 'user_id' obtenido del token.
            user = CustomUser.objects.filter(id=user_id).first()  # Usando el 'user_id' para obtener el usuario.
            if not user:
                # Si no se encuentra el usuario, responde con un error 401.
                return JsonResponse({'error': 'Unauthorized - User not found'}, status=401)

            # Si el usuario es válido, asigna el usuario autenticado al objeto 'request' para que esté disponible
            # en las vistas posteriores.
            request.user = user  # Esto asigna el usuario autenticado al request para usarlo en la vista.

        except TokenError:
            # Si el token no es válido o hay algún error al decodificarlo, responde con un error 401.
            return JsonResponse({'error': 'Unauthorized - Invalid token'}, status=401)
        except Exception as e:
            # Si ocurre cualquier otro error, responde con un mensaje de error genérico.
            return JsonResponse({'error': f'Unauthorized - {str(e)}'}, status=401)

        # Si todo está bien, llama a la vista original pasando los parámetros correspondientes.
        return view_func(request, *args, **kwargs)

    return _wrapped_view  # Devuelve la vista envuelta con la lógica de autenticación.
