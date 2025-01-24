

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand


# from scripts.database_fixes.fix_main_image import update_fix_main_image
from scripts.inits.load_ecommerce import load_store_init 


class Command(BaseCommand):
    help = "Es un comando exclusivamente para ejecutar algunos scripts que no se podian ejecutar en railway"
    
    def handle(self, *args, **kwargs):
        # update_fix_main_image()
        load_store_init()