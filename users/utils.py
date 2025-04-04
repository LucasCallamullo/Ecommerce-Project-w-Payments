

import requests
from django.conf import settings

def get_url_from_imgbb(request):
    # image = request.FILES["image"].read()
    image = request.FILES["image"]
    api_key = settings.IMGBB_KEY
    response = requests.post(
        "https://api.imgbb.com/1/upload",
        params={"key": api_key},
        files={"image": image}
    )

    data = response.json()
    if data["success"]:
        return data["data"]["url"]
        
    # Si no retornara None por defecto en cualquier caso
    return None


from django.template.loader import render_to_string
from home.models import Store, HeaderImages, BannerImages
from django.db.models import Prefetch

def get_first_tab_render(request):
    # Obtener el store con prefetch optimizado
    store = Store.objects.prefetch_related(
        Prefetch('headers', 
            queryset=HeaderImages.objects.filter(soft_delete=False),
            to_attr='active_headers'
        ),
        Prefetch('headers',
            queryset=HeaderImages.objects.filter(soft_delete=True),
            to_attr='inactive_headers'
        ),
        Prefetch('banners',
            queryset=BannerImages.objects.filter(soft_delete=False),
            to_attr='active_banners'
        ),
        Prefetch('banners',
            queryset=BannerImages.objects.filter(soft_delete=True),
            to_attr='inactive_banners'
        )
    ).filter(id=1).first()

    # Pasar los datos al contexto para el template
    context = {
        'store': store,
        # Listas ya filtradas en el prefetch mejor performance
        'headers_active': store.active_headers,  
        'headers_inactive': store.inactive_headers,
        'banners_active': store.active_banners,
        'banners_inactive': store.inactive_banners
    }
        
    return render_to_string('users/tabs/headers_adm.html', context, request=request)