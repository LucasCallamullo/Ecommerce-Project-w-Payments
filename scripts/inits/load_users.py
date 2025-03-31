

import os, sys, django

# Agrega el directorio raíz del proyecto al PYTHONPATH para que Django encuentre los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()


from django.contrib.auth.hashers import make_password
from users.models import CustomUser


def load_users_init():
    # Crear superusuario
    user, created = CustomUser.objects.get_or_create(
        email="admin@gmail.com",
        defaults={
            "password": make_password("1234"),
            "first_name": "Admin",
            "last_name": "SuperAdmin",
            "is_active": True,
            "is_staff": True,
            "is_superuser": True,
        }
    )
    
    if created:
        print(f'El Super usuario {user.email} Se creo exitosamente')

    # Crear usuarios de ejemplo
    users = [
        {"email": "user1@gmail.com", "first_name": "Lucas", "last_name": "Martinez"},
        {"email": "user2@gmail.com", "first_name": "Ariana", "last_name": "Romero"},
        {"email": "user3@gmail.com", "first_name": "Agos", "last_name": "Pereyra"},
    ]
    
    for user_data in users:
        user, created = CustomUser.objects.get_or_create(
            email=user_data["email"],
            defaults={
                "password": make_password("1234"),
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "is_active": True,
            }
        )
        
        if created:
            print(f'El usuario {user.email} Se creo exitosamente')
        else:
            print(f"El usuario {user.email} ya existia")

    
if __name__ == "__main__":
    load_users_init()







