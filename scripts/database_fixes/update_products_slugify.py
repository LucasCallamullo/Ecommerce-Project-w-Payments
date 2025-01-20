

# python manage.py update_w_slugify
import os, sys
import django

# Agrega el directorio raíz del proyecto al PYTHONPATH para que Django encuentre los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()


""" 
    Se utilizo para actualizar los slugs en los productos recuperados desde el excel.
"""
import pandas as pd
from django.core.management.base import BaseCommand
from productos.models import Product
from django.utils.text import slugify


    

# Ruta al archivo Excel
file_path = 'productos/data/productos.xlsx'
df = None

try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f'Archivo no encontrado: {file_path}')


# Obtener datos del Excel
for index, row in df.iterrows():
    name = row.get("name")
    stock = row.get("stock")
    
    # Generación del slug único
    slug = slugify(name)
    original_slug = slug
    counter = 1
    while Product.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{counter}"
        counter += 1

    # Verificar si el producto ya existe
    product_obj = Product.objects.filter(name=name).first()
    
    if product_obj:
        # Si el producto existe, actualizar el stock y slug
        product_obj.stock = stock
        # Solo actualizar el slug si es necesario
        if product_obj.slug != slug:  
            product_obj.slug = slug
        product_obj.save()
        print(f'Producto {name} actualizado exitosamente.')
        
        
    else:
        # Si el producto no existe, crear uno nuevo
        Product.objects.create(
            name=name,
            stock=stock,
            slug=slug,
        )
        print(f'Producto {name} creado exitosamente.')
    
    
