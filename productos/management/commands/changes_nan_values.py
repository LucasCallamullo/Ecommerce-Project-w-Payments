from django.core.management.base import BaseCommand
from productos.models import Product, PBrand, PCategory, PSubcategory, ProductImage

# python manage.py changes_nan_values


class Command(BaseCommand):
    help = 'Reemplaza los valores "nan" por None en los campos de la base de datos'

    def handle(self, *args, **kwargs):
        # Procesa los productos
        productos = Product.objects.all()
        fields_products = ['category', 'subcategory', 'brand']
        self.generic_change_nan_value(productos, fields_products)
        
        # Procesa las marcas
        fields_generic = ['name', 'slug']
        brands = PBrand.objects.all()
        self.generic_change_nan_value(brands, fields_generic)
        
        # Procesa las categorías
        categories = PCategory.objects.all()
        self.generic_change_nan_value(categories, fields_generic)
        
        # Procesa las subcategorías
        subcategories = PSubcategory.objects.all()
        fields_generic.append('category')  # Añadir 'category' para subcategorías
        self.generic_change_nan_value(subcategories, fields_generic)
        
        # Procesa las imágenes
        fields_images = ['image', 'image_url'] 
        images = ProductImage.objects.all()
        self.generic_change_nan_value(images, fields_images)
        
        # Imprimir mensaje de éxito al final
        self.stdout.write(self.style.SUCCESS('Se han actualizado los valores "nan" a None en los campos especificados.'))

    def generic_change_nan_value(self, query, list_fields):
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