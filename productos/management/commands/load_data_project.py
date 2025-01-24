

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand

from productos.models import Product, PCategory, PSubcategory, PBrand, ProductImage

from scripts.inits.load_users import load_users_init
from scripts.inits.load_orders import load_orders_init
from scripts.inits.load_ecommerce import load_ecommerce_init


# command python manage.py load_data_project
def clean_value(value, zero=False):
    """
        Limpia los valores nulos o vacíos y los convierte a None o Zero segun corresponda 
        para la base de datos y almacenalos correctamente

    Args:
        value (any): El valor que se obtiene de la fuente de datos (por ejemplo, un archivo Excel).
        zero (bool): es para habilitar que se devuelvan 0 en lugar de None para campos numericos.

    Returns:
        Retorna un valor valido o None o Zero segun corresponda
    """
    result = None if pd.isna(value) or value == '' else value
    
    if zero:
        return 0 if result is None else result
    
    return result


class Command(BaseCommand):
    help = "Para cargar de forma generica todos los datos de modelos que creamos necesarios "
    help += "en este caso se incluyen los modelos de Productos desde el excel hacia la base de datos. "
    help += "Por otro lado simplemente se uso diccionarios para crear modelos ejemplos de Store, User, Orders"
        
    def handle(self, *args, **kwargs):

        # Ruta al archivo Excel
        try:
            file = 'productos/data/products_data.xlsx'
            
        except FileNotFoundError:
            print(f'Archivo no encontrado: {file}')
            return None
        
        # Obtener datos de los productos del excel del excel 
        df = pd.read_excel(file)

        for index, row in df.iterrows():
            name = clean_value(row.get("name"))
            
            if not name:
                print(f'Producto "{index}" no tiene product_name.')
                continue
                
            category = clean_value(row.get("category"))
            subcategory = clean_value(row.get("subcategory"))
            brand = clean_value(row.get("brand"))
            
            # Crear categorías, subcategorias, marcas si no existen
            category_obj = None
            if category is not None:
                category_obj, _ = PCategory.objects.get_or_create(name=category)
                    
            sub_category_obj = None
            if subcategory is not None:
                sub_category_obj, created = PSubcategory.objects.get_or_create(name=subcategory, category=category_obj)
            
            brand_obj = None
            if brand is not None:
                brand_obj, _ = PBrand.objects.get_or_create(name=brand)
            
            # Obtenemos el resto de valores del excel
            price = clean_value(row.get("price"), zero=True)
            stock = clean_value(row.get("stock"), zero=True)
            discount = clean_value(row.get("discount"), zero=True)
            
            # return true or false para la disponibilidad
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
            
            # agregamos las imagenes url a los productos
            cont = 0
            if image_url:
                ProductImage.objects.create(product=product_obj, image_url=image_url)
                cont += 1
        
            if image_url2:
                ProductImage.objects.create(product=product_obj, image_url=image_url2)
                cont += 1
                
            if created:
                print(f'Se creo correctamente el producto {product_obj.name} con {cont} imagenes asociadas.')
            else:
                print(f'Se actualizo correctamente el producto {product_obj.name} con {cont} imagenes asociadas.')
             
        # ================================================================
        # Crear otros datos necesarios para la carga inicial del proyecto
        print("=" * 50)
        # Esto llama a la funcion en scripts/ para cargar las orders iniciales
        load_orders_init()
        
        print("=" * 50)
        # Esto llama a la funcion en scripts/ para cargar los Users iniciales
        load_users_init()
        
        print("=" * 50)
        # Esto llama a la funcion en scripts/ para cargar los Users iniciales
        load_ecommerce_init()
        
        
        
        
        