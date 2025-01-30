

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import CustomUser


class MyCustomJWTAuthentication(JWTAuthentication):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = CustomUser
    
    
    def authenticate(self, request):
        """
        Autentica al usuario leyendo el token de la cookie en lugar del header Authorization.
        """
        token = request.COOKIES.get("access_token")  # Obtener el token de la cookie

        if not token:
            return None  # No hay token, sigue con la autenticación normal

        try:
            validated_token = self.get_validated_token(token)
            return self.get_user(validated_token), validated_token
        except AuthenticationFailed:
            return None  # Token inválido, no autenticar al usuario
