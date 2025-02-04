from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

# DRF n JWT stuff
from datetime import timedelta
from django.conf import settings


# Custom User Manager que se encarga de la creación de usuarios y superusuarios
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Si no se proporciona un email, se genera un error
        if not email:
            raise ValueError('The Email field must be set')
        
        # Normaliza el email para que tenga el formato correcto
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # Se establece la contraseña cifrada
        user.set_password(password)
        # Guarda el usuario en la base de datos
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Asegura que los superusuarios tengan ciertos permisos
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Llama a la creación del usuario normal para el superusuario
        return self.create_user(email, password, **extra_fields)


# Modelo de usuario personalizado que reemplaza al modelo por defecto de Django
class CustomUser(AbstractUser):
    """
    Notes: 
        Para el futuro saber que este modelo se pudo realizar con migraciones personalizadas,
        primero hacer makemigrations y despues consultar como seguir en base a los campos 
        eliminados y/o faltantes, ver ejemplo en users/migrations/0002_xxx
        
        En caso de que salga un error de inconsistencia de migraciones como este
            django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial 
            is applied before its dependency users.0001_initial on database 'default'.
        
        la solucion más proxima es ir a 
            # settigs.py y comentar la app del admin
                # 'django.contrib.admin',
                
            # urls.py tambien ir y comentar el include del admin
                # path('admin/', admin.site.urls),
                
            # aplicar migraciones con alguna personalizada, como la anterior
                # makemigrations (opcional)
                # migrate users
            
            # descomentar todo lo anterior(lo de admin) y volver a realizar migraciones
                # makemigrations
                # migrate 
        
        fuente: 
            https://stackoverflow.com/questions/44651760/django-db-migrations-exceptions-inconsistentmigrationhistory
    """
    
    # Elimina el campo 'username' del modelo predeterminado
    username = None 
    
    email = models.EmailField(unique=True)  # El campo de email es único para cada usuario
    cellphone = models.CharField(max_length=20, blank=True, null=True)  # Número de teléfono (opcional)
    province = models.CharField(max_length=50, blank=True, null=True)  # Provincia del usuario (opcional)
    address = models.CharField(max_length=255, blank=True, null=True)  # Dirección del usuario (opcional)
    
    """ 
    Otros campos
    first_name: Primer nombre del usuario.
    last_name: Apellido del usuario.
    is_active: Booleano que indica si el usuario está activo.
    is_staff: Booleano que indica si el usuario tiene permisos de administrador.
    is_superuser: Booleano que indica si el usuario es un superusuario.
    last_login: Fecha y hora de la última vez que el usuario inició sesión.
    date_joined: Fecha y hora en que el usuario se registró.
    groups: Grupos a los que pertenece el usuario.
    user_permissions: Permisos específicos asignados al usuario.
    """
    
    # Usa el email en lugar de 'username' para la autenticación
    USERNAME_FIELD = "email"

    # No se requieren campos adicionales para crear un superusuario (por defecto solo se necesita email y password)
    REQUIRED_FIELDS = []  # Si agregas campos adicionales, colócalos aquí

    # Se asigna el CustomUserManager para gestionar la creación de usuarios
    objects = CustomUserManager()

    # Método para representar el usuario como una cadena (usando el email)
    def __str__(self):
        return self.email  # Devuelve el correo electrónico como representación del usuario