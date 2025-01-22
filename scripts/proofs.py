


import mercadopago

import os, sys
import django

# Agrega el directorio raíz del proyecto al PYTHONPATH para que Django encuentre los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()


items = [
        {
            "title": "Producto 1",
            "quantity": 3,
            "unit_price": 100.00,
            "currency_id": "BRL",
            "picture_url": "https://www.mercadopago.com/org-img/MP3/home/logomp3.gif",
            "description": "Descrição do Item",
            "category_id": "art",
        },
        {
            "title": "Producto 2",
            "quantity": 1,
            "unit_price": 50.00,
            "currency_id": "BRL",
            "picture_url": "https://www.mercadopago.com/org-img/MP3/home/logomp3.gif",
            "description": "Descrição do Item",
            "category_id": "art",
        }
    ]

    # Aplicar descuento de $20
descuento = 20.00
total = sum(item["unit_price"] * item["quantity"] for item in items)
total_con_descuento = total - descuento

# Recalcular precios proporcionalmente
for item in items:
    item["unit_price"] -= (descuento / total) * item["unit_price"]
    
    
# Recalcular precios proporcionalmente
for item in items:
    print(f"el {item["title"]} vale {item["unit_price"]} ")
    
total = sum(item["unit_price"] * item["quantity"] for item in items)
print(total)
    
    
    
