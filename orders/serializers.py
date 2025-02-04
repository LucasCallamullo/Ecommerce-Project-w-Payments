

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class OrderFormSerializer(serializers.Serializer):
    """
    Este es el formulario para almacenar temporalmente los datos de una orden
    """
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    cellphone = serializers.CharField()
    dni = serializers.CharField()
    detail_order = serializers.CharField()

    # Campos de dirección, inicialmente no son obligatorios
    province = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    postal_code = serializers.CharField(required=False)
    detail = serializers.CharField(required=False)
    
    # Campos de retiro en local, inicialmente no son obligatorios
    name_retiro = serializers.CharField(required=False)
    dni_retiro = serializers.CharField(required=False)

    # Método de envío
    id_envio_method = serializers.CharField()

    def validate(self, data):
        # Campos dependiendo del método de envío
        envio_fields = ['province', 'city', 'address', 'postal_code', 'detail']
        retiro_fields = ['name_retiro', 'dni_retiro']
        
        envio_method = data.get("envio_method_id")  # Asegúrate de acceder correctamente al valor
        
        if envio_method in ["1", 1]:  # Si es retiro en local
            # Validar campos de retiro
            for field in retiro_fields:
                if not data.get(field, "").strip():
                    raise ValidationError(f"{field}: Este campo no puede estar vacío.")
        else:  # Si no es retiro, entonces deben ser los campos de dirección
            for field in envio_fields:
                if not data.get(field, "").strip():
                    raise ValidationError(f"{field}: Este campo no puede estar vacío.")
        
        return data
