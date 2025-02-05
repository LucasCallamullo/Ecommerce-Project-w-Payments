

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.serializers import OrderFormSerializer
from orders.utils import confirm_stock_available

class order_form(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder
    
    def post(self, request):

        print(request.data)  # for debug # Para ver qué datos realmente llegan
        serializer = OrderFormSerializer(data=request.data)

        if serializer.is_valid():
            # Confirmar pedido y hacer reserva de stock:
            confirm_stock = confirm_stock_available(request.user.id)
            if confirm_stock is False:
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
            
            # recuperamos el json de Datos ya validados
            order_data = serializer.validated_data  
            
            # Guardar en la sesión del usuario
            request.session['order_data'] = order_data
            request.session.modified = True  # Asegurar que Django guarde los cambios

            return Response({"success": True}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
