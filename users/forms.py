

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

from users.models import CustomUser
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


class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'province', 'address']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'province': forms.Select(choices=PROVINCIAS_CHOICES),
        }

    phone = forms.CharField(max_length=20)
    address = forms.CharField(max_length=250, required=False)
    province = forms.ChoiceField(choices=PROVINCIAS_CHOICES, required=False)


class WidgetLoginForm(forms.Form):
    """
        Este es el formulario para logearse con una cuenta ya creada em el widget_registro
    """
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'required': True})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'required': True})
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            raise ValidationError('El email no está registrado.')
        return email


class CreateUserForm(forms.ModelForm):
    """
        Esto es parte del formulario para registrarse con una nueva cuenta en la hoja "Registro"
        Se hereda de forms.ModelForm para poder controlar el hecho de no utilizar password2 para autenticar
    """
    # le damos algunos formatos posibles
    email = forms.CharField(max_length=50, error_messages={
        'invalid': 'Ingrese una dirección de correo electrónico válida.'
    })
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=20)
    province = forms.ChoiceField(choices=PROVINCIAS_CHOICES, required=False)  # Campo opcional
    address = forms.CharField(max_length=250, required=False)  # Campo opcional

    # se realiza esto para "eliminar" la doble validacion de password
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = None

    class Meta:
        # declaramos nuestro .models CustomUser y le pasamos los campos a completar que recuperamos
        model = CustomUser
        fields = ('email', 'password1', 'first_name', 'last_name', 'phone', 'province', 'address')
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # les asignamos un tipo de clase a todos nuestros widgets p/ trabajar con css
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'user-create-form'})


    def save(self, commit=True):
        user = super().save(commit=False)
        # Configurar la contraseña encriptada
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


    def clean_password1(self):
        # Metodo necesario para poder eliminar la validacion doble del password2
        password1 = self.cleaned_data.get('password1')
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            # Method inherited from BaseForm
            self.add_error('password1', "Debe tener al menos 4 caracteres.")
        return password1


    def clean_email(self):
        # metodo necesario para poder autenticar el email
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email









