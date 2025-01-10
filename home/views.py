from django.shortcuts import render

# Create your views here.
from home.models import Ecommerce, E_HeaderImages, E_BannerImages


def home(request):
    
    return render(request, "home/home.html")