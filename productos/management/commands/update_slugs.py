

"""
for producto in productos:
        if not producto.slug:
            producto.slug = slugify(producto.name)
            producto.save()
"""

# python manage.py update_slugs
from django.core.management.base import BaseCommand
from productos.models import Product, PBrand, PCategory, PSubcategory
from django.utils.text import slugify


def update_slugsss(query_set):
    cont = 0

    for obj in query_set:
        # Verifica que 'name' no sea nulo, vacío o un valor no válido como 'nan'
        if not obj.slug and obj.name and obj.name.strip().lower() != "nan":
            obj.slug = slugify(obj.name)
            obj.save()
            cont += 1
            print("Objeto actualizado:", obj.name)
    
    if cont > 0:
        print(f"Se actualizaron {cont} objetos del queryset {query_set.model.__name__}.")
    else:
        print(f"No se encontraron objetos sin slug en el queryset {query_set.model.__name__}.")



class Command(BaseCommand):
    help="Se realizo en su momento para actualizar algunos slug faltantes"

    def handle(self, *args, **kwargs):
        productos = Product.objects.all()
        categories = PCategory.objects.all()
        sub_categories = PSubcategory.objects.all()
        brands = PBrand.objects.all()

        update_slugsss(productos)
        update_slugsss(categories)
        update_slugsss(sub_categories)
        update_slugsss(brands)
