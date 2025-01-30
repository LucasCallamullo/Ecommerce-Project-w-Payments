

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.utils import timezone
import json
from datetime import timedelta



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            
            
            data = serializer.validated_data
            response = Response(data)
            
            login(request, data["user"])
            
            expires = timezone.now() + timedelta(days=1)

            response.set_cookie(
                key='access_token',
                value=data["tokens"]['access'],
                httponly=True,
                samesite='Lax',  # 'Lax' debería funcionar para la mayoría de los casos locales
                expires=expires,
                secure=settings.SECURE_SSL_REDIRECT if not settings.DEBUG else False,
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated




from django.http import JsonResponse
from rest_framework import status
from users.serializers import LoginSerializer


from rest_framework.response import Response
from rest_framework.decorators import api_view



from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from django.contrib.auth import login
# login(request, request.user) 

class LoginView322(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            response = Response(data)  # Usa Response de DRF aquí en lugar de JsonResponse
            
            
            
            # Configurar la cookie para el token de acceso
            # expires = timezone.now() + timedelta(days=1)  # Configura la duración que desees para el JWT
            max_age = timedelta(days=1)  # Define la duración de la cookie
            
            response.set_cookie(
                key='access_token',
                value=data["tokens"]['access'],  # Usa el token de acceso del diccionario
                httponly=True,  # La cookie solo es accesible por el servidor, "none" si estan separados front y back
                samesite='Lax',  # Asegura que la cookie solo se envíe en el mismo sitio
                # expires=expires,  # Fecha de expiración
                max_age=max_age,  # Duración de la cookie
                secure=settings.SECURE_SSL_REDIRECT if not settings.DEBUG else False,  # Solo se envía por HTTPS en producción
            )

            return response  # Devuelve la respuesta correctamente

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados con JWT

    def get(self, request):
        return Response({"message": "¡Estás autenticado con JWT!"})
