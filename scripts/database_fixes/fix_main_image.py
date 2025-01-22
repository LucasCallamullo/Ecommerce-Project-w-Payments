

import os, sys, django

# Agrega el directorio raíz del proyecto al PYTHONPATH para que Django encuentre los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()


from productos.models import Product

def update_fix_main_image():
    
    productos = Product.objects.all()

    for product in productos:

        if product.images.exists():
            
            images = product.images.all()
            
            # Intentar obtener la imagen principal
            main_image = images.filter(main_image=True).first()
            
            if not main_image:
                image = images.first()
                image.main_image = True
                image.save()
                print(f"se cambio correctamente el main_image del {product.name}")
        
    
    




