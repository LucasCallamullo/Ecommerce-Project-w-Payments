

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from productos.models import Product, PCategory, PSubcategory, PBrand, ProductImage


""" 
    Comando incial, de python para cargar valores desde el excel queda abandonado en esta carpeta 
    porque ya no sirve tuvo muchas actualizaciones
"""



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
        
        # Leer el archivo Excel con pandas
        # recover False = Internet, True = Local
        recover = False
        file = self.file_local_or_internet(recover)
        df = pd.read_excel(file)

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
            
            # Si el producto ya existe, actualizar las imagenes
            if not created:
                
                # Corroboramos que las urls no se repitan y se creen otra imagen si ya existe
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
                 
            # Si el producto es nuevo, crear las imágenes   
            else:
                if image_url:
                    ProductImage.objects.create(
                        product=product_obj,
                        image_url=image_url
                    )
                
                if image_url2:
                    ProductImage.objects.create(
                        product=product_obj,
                        image_url=image_url2
                    )

    def file_local_or_internet(self, config_value=True):
        # recupera de forma local el archivo
        if config_value:
            # Ruta al archivo Excel
            file_path = 'productos/data/products_data.xlsx'
            try:
                return file_path
                
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(f'Archivo no encontrado: {file_path}'))
                return None
            
        """ 
        import os
        import gdown
        # Recupera el archivo desde internet
        # Opcion para pip install gdown ver mas opciones en el futuro
        else:
            # ID del archivo de Google Drive
            file_id = '150xsU_LQxn9W7Q_kaBKQFkpavj_Tu2sl'

            # Generar la URL de descarga directa
            url = f'https://drive.google.com/uc?id={file_id}'

            # Construir la ruta de la carpeta 'productos/data/' dentro del proyecto
            output_dir = os.path.join(settings.BASE_DIR, 'productos', 'data')
            
            # Crear la carpeta donde se guardará el archivo descargado si no existe
            os.makedirs(output_dir, exist_ok=True)
            
            # Ruta completa donde se guardará el archivo descargado
            output = os.path.join(output_dir, 'products_data.xlsx')
            
            # Verificar si el archivo ya existe
            if not os.path.exists(output):
                # Descargar el archivo a un archivo local
                try:
                    gdown.download(url, output, quiet=False)
                    return output
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error al descargar el archivo desde internet: {str(e)}'))
                    return None
            else:
                print(f"El archivo '{output}' ya existe. No se descargará.")
                return output
        """
            
            
                
            