

import os, sys, django

# Agrega el directorio raíz del proyecto al PYTHONPATH para que Django encuentre los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from home.models import Store, HeaderImages, BannerImages


def load_store_init():

    # Crear algunos datos iniciales para la tienda unica
    store, _ = Store.objects.get_or_create(
        name= "Cat Cat Games",
        wsp_number = "+54 9 351 543-7688",
        address = "Calle Falsa 123",
        cellphone = "351 543-7688",
        email = "cat_cat_games@gmail.com",
    )
    
    # agregar headers imagenes al ecommerce iniciales
    list_headers = [
        "https://redragon.es/content/uploads/2021/10/HEROS-S129W-BA.jpg",
        "https://sigmatiendas.com/cdn/shop/files/Logitech_banner_product_page_v2.jpg?v=1711139345&width=2800",
        "https://assets2.razerzone.com/images/pnx.assets/4b93db266e7ee65c3a25a5ae582ed586/razer-affiliate-hero-mobile.jpg"
    ]
    
    for header in list_headers:
        imagen, create = HeaderImages.objects.get_or_create(store=store, image_url=header)
        if create:
            print(f"se agrego el header_image con {imagen.image_url}")
    
    
    list_banners = [
        "https://www.techgames.com.mx/wp-content/uploads/2021/10/Logitech-G-y-Riot-Games-LOL.jpg",
        "https://redragonshop.com/cdn/shop/files/referal-candy-banner-m.png?v=1709540400"
    ]
    
    for header in list_banners:
        imagen, create = BannerImages.objects.get_or_create(store=store, image_url=header)
        if create:
            store.banner_image = imagen
            print(f"se agrego el banner_image con {imagen.image_url}")