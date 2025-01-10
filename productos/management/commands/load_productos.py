

import pandas as pd
from django.core.management.base import BaseCommand
from productos.models import Product, PCategory, PSubcategory, PBrand, ProductImage


# command python manage.py load_productos
def clean_value(value):
    """
    Limpia los valores nulos o vacíos y los convierte a None para la base de datos.

    Esta función verifica si el valor proporcionado es nulo o una cadena vacía,
    y en ese caso, lo convierte a `None`, lo cual es adecuado para su almacenamiento en la base de datos.
    Si el valor es válido, lo devuelve tal cual.

    Args:
        value (any): El valor que se obtiene de la fuente de datos (por ejemplo, un archivo Excel).

    Returns:
        any: El valor limpio, que puede ser `None` o el valor original si es válido.
    """
    return None if pd.isna(value) or value == '' else value


def clean_value_zero(value):
    """
    Limpia los valores nulos o vacíos y los convierte a 0 para la base de datos.

    Esta función verifica si el valor proporcionado es nulo o una cadena vacía,
    y en ese caso, lo convierte a `0`, lo cual es adecuado cuando se espera un valor numérico.
    Si el valor es válido, lo devuelve tal cual.

    Args:
        value (any): El valor que se obtiene de la fuente de datos (por ejemplo, un archivo Excel).

    Returns:
        int: `0` si el valor es nulo o vacío, o el valor original si es válido.
    """
    result = None if pd.isna(value) or value == '' else value
    return 0 if result is None else result


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
            name = clean_value(row.get("name"))
            if not name:
                self.stdout.write(self.style.SUCCESS(f'Producto "{index}" dont have product_name.'))
                continue
                
            category = clean_value(row.get("category"))
            subcategory = clean_value(row.get("subcategory"))
            brand = clean_value(row.get("brand"))
            
            # Crear categorías, subcategorias, marcas si no existen
            category_obj, _ = PCategory.objects.get_or_create(name=category)
            sub_category_obj, created = PSubcategory.objects.get_or_create(name=subcategory, category=category_obj)
            brand_obj, _ = PBrand.objects.get_or_create(name=brand)
            
            price = clean_value_zero(row.get("price"))
            price = 0 if price is None else price
            
            stock = clean_value_zero(row.get("stock"))
            stock = 0 if price is None else stock
            
            discount = clean_value_zero(row.get("discount"))
            discount = 0 if discount is None else discount
            
            # return true or false
            available_str = row.get("available", "").lower()
            available = available_str in ["si", "sí", "yes"]

            description = clean_value(row.get("description"))
            image_url = clean_value(row.get("image_url"))
            image_url2 = clean_value(row.get("image_url2"))

            # Recuperar o crear el producto
            product_obj, created = Product.objects.get_or_create(
                name=name,
                price=price,
                stock=stock,
                discount=discount,
                available=available,
                category=category_obj,
                subcategory=sub_category_obj,
                brand=brand_obj,
                description=description,
            )
            
            self.stdout.write(self.style.SUCCESS(f'Producto "{product_obj.name}" se creo correctamente.'))

            # Si el producto ya existe, actualizar el stock
            if not created:
                existing_images = product_obj.images.all()
                
                if image_url and not existing_images.filter(image_url=image_url).exists():
                    ProductImage.objects.create(
                        product=product_obj,
                        image_url=image_url
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Producto "{product_obj.name}" update image_url.')
                    )
                
                if image_url2 and not existing_images.filter(image_url=image_url2).exists():
                    ProductImage.objects.create(
                        product=product_obj,
                        image_url=image_url2
                    )
        
                    self.stdout.write(
                        self.style.SUCCESS(f'Producto "{product_obj.name}" update image_url2.')
                    )
                    
            else:
                # Si el producto es nuevo, crear las imágenes
                if image_url:
                    ProductImage.objects.create(
                        product=product_obj,
                        image_url=image_url,
                        main_image=True
                    )
                
                if image_url2:
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