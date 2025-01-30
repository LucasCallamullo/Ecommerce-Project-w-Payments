

from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        
        if not user:
            raise AuthenticationFailed('Email o Contraseña invalida, por favor verifique sus datos.')

        # Si la autenticación es exitosa, devuelve un diccionario con los datos del usuario y los tokens
        tokens = user.tokens()  # Obtén los tokens del usuario

        return {
            'email': user.email,
            
            'tokens': tokens,
            'redirect_url': '/profile_page/'
        }



class LoginSerializer32(serializers.Serializer):
    # Definición de los campos que recibirá el formulario de login
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """
        Este método se encarga de validar los datos de entrada (email y password).
        Si la autenticación es exitosa, devuelve los tokens del usuario.
        Si falla, lanza una excepción de autenticación.
        """
        email = data.get('email')  # Obtiene el correo electrónico de los datos
        password = data.get('password')  # Obtiene la contraseña de los datos

        # Intenta autenticar al usuario usando el email y la contraseña proporcionados
        user = authenticate(email=email, password=password)
        
        # Si la autenticación falla (usuario no encontrado o credenciales incorrectas)
        if not user:
            # Lanza una excepción de autenticación con un mensaje de error
            raise AuthenticationFailed('Email o Contraseña invalida, por favor verifique sus datos.')

        # Si la autenticación es exitosa, devuelve un diccionario con los datos del usuario y los tokens
        tokens = user.tokens()  # Obtén los tokens del usuario

        return {
            'email': user.email,
            'tokens': tokens,  # Devuelve los tokens de access y refresh del usuario
            'redirect_url': '/profile_page/'
        }


