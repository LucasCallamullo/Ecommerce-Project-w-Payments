

from django import forms
from django.core.exceptions import ValidationError


PROVINCIAS_CHOICES = [
    ('', 'Selecciona una provincia'),
    ('Buenos Aires', 'Buenos Aires'),
    ('Catamarca', 'Catamarca'),
    ('Chaco', 'Chaco'),
    ('Chubut', 'Chubut'),
    ('CABA', 'Ciudad Autónoma de Buenos Aires'),
    ('Córdoba', 'Córdoba'),
    ('Corrientes', 'Corrientes'),
    ('Entre Ríos', 'Entre Ríos'),
    ('Formosa', 'Formosa'),
    ('Jujuy', 'Jujuy'),
    ('La Pampa', 'La Pampa'),
    ('La Rioja', 'La Rioja'),
    ('Mendoza', 'Mendoza'),
    ('Misiones', 'Misiones'),
    ('Neuquén', 'Neuquén'),
    ('Río Negro', 'Río Negro'),
    ('Salta', 'Salta'),
    ('San Juan', 'San Juan'),
    ('San Luis', 'San Luis'),
    ('Santa Cruz', 'Santa Cruz'),
    ('Santa Fe', 'Santa Fe'),
    ('Santiago del Estero', 'Santiago del Estero'),
    ('Tierra del Fuego', 'Tierra del Fuego'),
    ('Tucumán', 'Tucumán')
]


from django import forms

class OrderForm(forms.Form):
    """
    Este es el formulario para almacenar temporalmente los datos de una orden
    """
    name = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su Nombre'})
    )
    last_name = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su Apellido'})
    )
    cellphone = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su Número'})
    )
    email = forms.EmailField(
        max_length=50, 
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su E-mail'})
    )
    dni = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su DNI'})
    )
    detail_order = forms.CharField(
        max_length=50, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese detalles del pedido'})
    )
    
    # otras formas de retiro
    province = forms.ChoiceField(
        choices=PROVINCIAS_CHOICES, 
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-obligado'
        })
    )

    city = forms.CharField(
        max_length=50, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese la ciudad'})
    )
    address = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese la dirección'})
    )
    postal_code = forms.CharField(
        max_length=20, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese el código postal'})
    )
    detail = forms.CharField(
        max_length=255, 
        required=False, 
        widget=forms.Textarea(attrs={
            'placeholder': 'Detalles adicionales del envío',
            'class': 'form-obligado'
        })
    )
    
    # retiro local
    name_retiro = forms.CharField(
        max_length=50, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de quien retira'})
    )
    dni_retiro = forms.CharField(
        max_length=50, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'DNI de quien retira'})
    )
    
    
    def __init__(self, *args, id_envio_method=None, **kwargs):
        """
        Constructor del formulario para ajustar dinámicamente los campos requeridos
        según el método de envío seleccionado.
        """
        super().__init__(*args, **kwargs)

        # Configuración dinámica de campos
        envio_fields = ['province', 'city', 'address', 'postal_code']
        retiro_fields = ['name_retiro', 'dni_retiro']

        # Retiro en local
        if id_envio_method == "1":  
            for field in envio_fields:
                self.fields[field].required = False
            for field in retiro_fields:
                self.fields[field].required = True
        
        # Envío a domicilio
        else:  
            for field in envio_fields:
                self.fields[field].required = True
            for field in retiro_fields:
                self.fields[field].required = False