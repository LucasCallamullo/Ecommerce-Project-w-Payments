

# python manage.py update_w_slugify
import os, sys
import django

# Agrega el directorio raíz del proyecto al PYTHONPATH para que Django encuentre los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()


"""
    este script se utilizo para limpiar ciertos campos nulos / "nan" que se guardaron al principio
    por error en la recuperacion de datos, no deberían de volver a pasar ya que se verificaron 
    todas las inconsistencias en el comando de la app productos load_data
    
    pero lo dejamos por si llegara a ser util en un futuro
"""


from productos.models import Product, PBrand, PCategory, PSubcategory, ProductImage


def generic_change_nan_value(query, list_fields):
    # Reemplaza los valores "nan" por None en los campos de cada objeto
    for obj in query:
        updated = False

        for field in list_fields:
            value = getattr(obj, field)

            # Si el valor es la cadena "nan", reemplázalo por None
            if value == "nan":
                setattr(obj, field, None)
                updated = True

        if updated:
            obj.save()


# Procesa los productos
productos = Product.objects.all()
fields_products = ['category', 'subcategory', 'brand']
generic_change_nan_value(productos, fields_products)

# Procesa las marcas
fields_generic = ['name', 'slug']
brands = PBrand.objects.all()
generic_change_nan_value(brands, fields_generic)

# Procesa las categorías
categories = PCategory.objects.all()
generic_change_nan_value(categories, fields_generic)

# Procesa las subcategorías
subcategories = PSubcategory.objects.all()
fields_generic.append('category')  # Añadir 'category' para subcategorías
generic_change_nan_value(subcategories, fields_generic)

# Procesa las imágenes
fields_images = ['image', 'image_url'] 
images = ProductImage.objects.all()
generic_change_nan_value(images, fields_images)

# Imprimir mensaje de éxito al final
print('Se han actualizado los valores "nan" a None en los campos especificados.')

    
"""
class Command(BaseCommand):
    help = 'Reemplaza los valores "nan" o None en los campos de la base de datos por None'

    def handle(self, *args, **kwargs):
        # Procesa los productos
        productos = Product.objects.all()
        
        for product in productos:
            updated = False
            
            if product.category.name is None or product.subcategory.name is None:
                product.category = None
                product.subcategory = None
                updated = True
            
            elif product.brand.name is None:
                product.brand = None
                updated = True
                
            if updated:
                product.save()
                self.stdout.write(self.style.SUCCESS(f'Producto "{product.name}" actualizado.'))
"""