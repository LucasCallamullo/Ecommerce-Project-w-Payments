


import pandas as pd
from django.core.management.base import BaseCommand

from productos.models import Product, PCategory, PSubcategory, PBrand, ProductImage

# command python manage.py load_productos

class Command(BaseCommand):
    help = "Para cargar de forma generica los productos"

    def handle(self, *args, **kwargs):
        # Ruta al archivo Excel
        file_path = 'productos/data/productos.xlsx'
        try:
            df = pd.read_excel(file_path)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Archivo no encontrado: {file_path}'))
            return
        
        # Obtener datos del excel 
        for index, row in df.iterrows():
            name = row.get("name")
            price = row.get("price")
            stock = row.get("stock")
            
            available_str = row.get("available")
            available = True if available_str.lower() == "si" else False
            
            discount_value = row.get("discount")
            discount = pd.to_numeric(discount_value, errors='coerce')  # Coerce convierte a NaN si no es un número
            discount = discount if pd.notna(discount) else 0  # Reemplazar NaN por 0 si es necesario
            
            category = row.get("category")
            subcategory = row.get("subcategory")
            brand = row.get("brand")
            
            description = row.get("description")
            image_url = row.get("image_url")
            image_url2 = row.get("image_url2")

            # Crear categorías, subcategorias, marcas si no existen
            category_obj, _ = PCategory.objects.get_or_create(name=category)
            sub_category_obj, created = PSubcategory.objects.get_or_create(name=subcategory, category=category_obj)
            brand_obj, _ = PBrand.objects.get_or_create(name=brand)
            
            # Si la subcategoría ya existía, muestra un mensaje
            if not created:
                self.stdout.write(self.style.WARNING(f'Subcategory "{subcategory}" already exists, skipping creation.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Subcategory "{subcategory}" created successfully.'))
            
            # Recuperar o crear el producto
            product_obj, created = Product.objects.get_or_create(
                name=name,
                price=price,
                available=available,
                discount=discount,
                category=category_obj,
                subcategory=sub_category_obj,
                brand=brand_obj,
                description=description,
                stock=stock
            )

            # Si el producto ya existe, actualizar el stock
            if not created:
                existing_images = product_obj.images.all()
                self.stdout.write(self.style.SUCCESS(f'Producto "{product_obj.name}" update successfully.'))
                
                if not existing_images.filter(image_url=image_url).exists():
                    ProductImage.objects.create(
                        product=product_obj,
                        image_url=image_url,
                        main_image=True
                    )
                
                if not existing_images.filter(image_url=image_url2).exists():
                    ProductImage.objects.create(
                        product=product_obj,
                        image_url=image_url2,
                        main_image=False
                    )
            else:
                # Si el producto es nuevo, crear las imágenes
                ProductImage.objects.create(
                    product=product_obj,
                    image_url=image_url,
                    main_image=True
                )
                ProductImage.objects.create(
                    product=product_obj,
                    image_url=image_url2,
                    main_image=False
                )





''' 
import pandas as pd

# URL directa del archivo en Google Drive
url = 'https://drive.google.com/uc?id=YOUR_FILE_ID'

# Lee el archivo Excel directamente desde la URL
df = pd.read_excel(url)

print(df.head())
'''