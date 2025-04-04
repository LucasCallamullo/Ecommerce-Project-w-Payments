

from rest_framework.views import APIView
from rest_framework.response import Response  
from rest_framework import status  

from home.models import Store 
from home.serializers import UpdateStoreSerializer 

class StoreUpdateAPI(APIView):
    def post(self, request):
        # Verificar si es admin o superadmin
        if request.user.id != 1 and request.user.role != 'admin':
            return Response(
                {'detail': 'No tienes permisos para esta acción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obtiene el primer Store con id=1 de la base de datos
        # first() devuelve None si no encuentra ningún registro
        store = Store.objects.filter(id=1).first()

        # Crea una instancia del serializador para actualizar el Store:
        # 1er argumento: instancia del modelo a actualizar (store)
        # data: datos recibidos en la petición (request.data)
        # partial=True: permite actualización parcial (no todos los campos son requeridos)
        serializer = UpdateStoreSerializer(store, data=request.data, partial=True)
        
        # Verifica si los datos pasan las validaciones del serializador
        if serializer.is_valid():
            # Si son válidos, guarda los cambios en la base de datos
            serializer.save()
            # Devuelve los datos actualizados en la respuesta
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        # Si los datos no son válidos, devuelve los errores de validación
        # con código de estado HTTP 400 (Bad Request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)