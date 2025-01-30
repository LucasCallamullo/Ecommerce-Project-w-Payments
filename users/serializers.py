

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

