

import os
import sys
import django

# Agrega el directorio raíz del proyecto al PYTHONPATH para que Django encuentre los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()


"""
    Script generico desarrollado para actualizar la base de datos con slug en los modelos de la 
    app productos que ya fueron previamente creados
    además de realizar algunas verificaciones extra ya que algunos campos habían sido guardados
    sin tener en cuenta ciertas verifiaciones
"""
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


# objetos a realizar actualizacion
productos = Product.objects.all()
categories = PCategory.objects.all()
sub_categories = PSubcategory.objects.all()
brands = PBrand.objects.all()

update_slugsss(productos)
update_slugsss(categories)
update_slugsss(sub_categories)
update_slugsss(brands)
