

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from orders.models import ShipmentMethod, PaymentMethod

class PaymenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['name', 'time', 'is_active', 'description']
        read_only_fields = ['id']  # Lo marcamos como solo lectura
        extra_kwargs = {
            'name': {'required': False},
            'time': {'required': False},
            'is_active': {'required': False},
            'description': {'required': False},
        }
        
        
class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentMethod
        fields = ['name', 'price', 'is_active', 'description']
        read_only_fields = ['id']  # Lo marcamos como solo lectura
        extra_kwargs = {
            'name': {'required': False},
            'price': {'required': False},
            'is_active': {'required': False},
            'description': {'required': False},
        }


class OrderFormSerializer(serializers.Serializer):
    """
    This serializer is used to temporarily store order data from a form.
    
    It includes customer personal details, optional shipping or pickup 
    information, and payment method selection.
    """
    
    # Customer personal details
    first_name = serializers.CharField() 
    last_name = serializers.CharField()  
    email = serializers.EmailField()
    cellphone = serializers.CharField() 
    dni = serializers.CharField()
    detail_order = serializers.CharField(required=False, allow_blank=True)  
    # Optional order details (e.g., additional notes)

    # Shipping address fields (initially optional)
    province = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    postal_code = serializers.CharField(required=False, allow_blank=True) 
    detail = serializers.CharField(required=False, allow_blank=True)  
    # Additional address details (e.g., apartment number)

    # Local pickup details (initially optional)
    name_retire = serializers.CharField(required=False, allow_blank=True)  
    # Name of the person picking up the order
    dni_retire = serializers.CharField(required=False, allow_blank=True)  
    # ID number of the person picking up the order

    # Shipping and payment method selection
    shipping_method_id = serializers.CharField(required=False)  
    # ID of the selected shipping method
    payment_method_id = serializers.CharField(required=False)  
    # ID of the selected payment method

    def validate(self, data):
        shipping_fields = {
            'province': "Provincia",
            'city': "Ciudad",
            'address': "Dirección",
            'postal_code': "Código Postal",
            'detail': "Detalle"
        }

        retire_fields = {
            'name_retire': "Nombre quien retira",
            'dni_retire': "DNI quien retira"
        }

        # Get Shipping Method
        shipping_method = data.get("shipping_method_id")

        if shipping_method in ["1", 1]:  # If is local retire
            for field, translated_name in retire_fields.items():
                if not data.get(field, "").strip():
                    raise ValidationError({translated_name: "Este campo no puede estar vacío."})

        else:  # Si es envío a domicilio
            for field, translated_name in shipping_fields.items():
                if not data.get(field, "").strip():
                    raise ValidationError({translated_name: "Este campo no puede estar vacío."})

        return data
