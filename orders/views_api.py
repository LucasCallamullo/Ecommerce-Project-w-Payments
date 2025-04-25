

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from django.http import Http404
from django.shortcuts import get_object_or_404

from orders.serializers import OrderFormSerializer, ShipmentSerializer, PaymenSerializer
from orders.models import ShipmentMethod, PaymentMethod
from users.permissions import IsAdminOrSuperUser
from orders import utils

class EditPaymentView(APIView):
    # Verificar si es role == 'admin' o user.id == 1
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]
    
    def post(self, request):

        # Mejor forma de manejar el error si no existiera el objeto como tal
        try:
            payment = get_object_or_404(PaymentMethod, id=request.data.get("id"))
        except Http404:
            return Response({"success": False, "error": "El método de pago no existe."}, status=status.HTTP_404_NOT_FOUND)

        # mandar a validar con el serializador el json recibido desde el form
        serializer = PaymenSerializer(payment, data=request.data, partial=True)

        # si esta todo bien se guarda el objeto automaticamente
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Método de pago actualizado."}, status=status.HTTP_200_OK)
        
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        
class EditShipmentView(APIView):
    # Verificar si es role == 'admin' o user.id == 1
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]
    
    def post(self, request):
        
        # Mejor forma de manejar el error si no existiera el objeto como tal
        try:
            shipment = get_object_or_404(ShipmentMethod, id=request.data.get("id"))
        except Http404:
            return Response({"success": False, "error": "El método de envío no existe."}, status=status.HTTP_404_NOT_FOUND)

        # mandar a validar con el serializador el json recibido desde el form
        serializer = ShipmentSerializer(shipment, data=request.data, partial=True)

        # si esta todo bien se guarda el objeto automaticamente
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Shipment actualizado correctamente"}, status=status.HTTP_200_OK)
            
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

       
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
        
