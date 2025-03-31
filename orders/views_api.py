

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.serializers import OrderFormSerializer
from orders import utils

class order_form(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder
    
    def post(self, request):

        # print(request.data)  # for debug # Para ver qué datos realmente llegan
        serializer = OrderFormSerializer(data=request.data)

        if serializer.is_valid():
            
            # Confirmar pedido y hacer reserva de stock:
            confirm_stock = utils.confirm_stock_availability(request.user.id)
            if confirm_stock != 'continue':
                return Response({'success': confirm_stock}, status=status.HTTP_400_BAD_REQUEST)
            
            # recuperamos el json de Datos ya validados
            order_data = serializer.validated_data
            
            try:
                order, message = utils.create_order_pending(order_data, request)
                    
                if not order:
                    response_data = {'success': 'error', 'message': message}
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                    
                return Response({'order_id': order.id}, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                print(str(e))
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
