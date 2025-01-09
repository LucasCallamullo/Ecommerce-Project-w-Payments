

# python manage.py update_w_slugify

import pandas as pd
from django.core.management.base import BaseCommand
from productos.models import Product
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Para actualizar productos con el slugify que se agregó después"
    
    def handle(self, *args, **kwargs):
        # Ruta al archivo Excel
        file_path = 'productos/data/productos.xlsx'
        
        try:
            df = pd.read_excel(file_path)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Archivo no encontrado: {file_path}'))
            return
        
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
            product_obj = Product.objects.filter(name=name).first()  # Buscar por el nombre

            if product_obj:
                # Si el producto existe, actualizar el stock y slug
                product_obj.stock = stock
                if product_obj.slug != slug:  # Solo actualizar el slug si es necesario
                    product_obj.slug = slug
                product_obj.save()  # Guardar cambios
                self.stdout.write(self.style.SUCCESS(f'Producto {name} actualizado exitosamente.'))
                
                
            else:
                # Si el producto no existe, crear uno nuevo
                Product.objects.create(
                    name=name,
                    stock=stock,
                    slug=slug,
                )
                self.stdout.write(self.style.SUCCESS(f'Producto {name} creado exitosamente.'))
            
            
