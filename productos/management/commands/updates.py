

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand


# from scripts.database_fixes.fix_main_image import update_fix_main_image
from scripts.inits.load_ecommerce import load_store_init

from productos.models import Product
from productos import utils


class Command(BaseCommand):
    help = "Es un comando exclusivamente para ejecutar algunos scripts que no se podian ejecutar en railway"
    
    def handle(self, *args, **kwargs):
        # update_fix_main_image()
        # load_store_init()
        
        updates_normalized_names()
        
        
def updates_normalized_names():
    """
    Usar bulk_update es una forma más eficiente de actualizar varios objetos sin llamar a save() 
    en cada uno de ellos, especialmente cuando necesitas actualizar el mismo campo para muchos 
    registros.
    """
    
    products = Product.objects.all()
        
    for product in products:
        product.normalized_name = utils.normalize_or_None(product.name)
        print(f"name: {product.name} | normalized_name: {product.normalized_name}")
        
    # Usar bulk_update para actualizar todos los productos en una sola consulta
    Product.objects.bulk_update(products, ['normalized_name'])