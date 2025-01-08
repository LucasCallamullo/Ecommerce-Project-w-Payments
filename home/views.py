from django.shortcuts import render

# Create your views here.
from home.models import Ecommerce, E_HeaderImages, E_BannerImages


def home(request):
    try:
        ecommerce = Ecommerce.objects.get(id=1)  # Devuelve directamente el objeto
    except Ecommerce.DoesNotExist:
        ecommerce = None  # En caso de que no exista, lo manejamos
        
    if ecommerce is not None:
        header_images = E_HeaderImages.objects.all()
        banner_images = E_BannerImages.objects.all()
        
        
        
        context = {
            "ecommerce": ecommerce,
            'header_images': header_images,
            'banner_images': banner_images
        }
        return render(request, "home/home.html", context)
    
    else:
        return render(request, "home/home.html")