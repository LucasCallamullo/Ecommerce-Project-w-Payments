from django.shortcuts import render

# Create your views here.

from users.models import CustomUser
from productos.models import Product


def home(request):
    products = Product.objects.select_related('category').all()
    products_by_category = {}

    for product in products:
        category_name = product.category.name
        if category_name not in products_by_category:
            products_by_category[category_name] = []
        products_by_category[category_name].append(product)

    return render(request, 'home/home.html', {'products_by_category': products_by_category})


def help_mp(request):
    users = CustomUser.objects.filter(is_superuser=False)
    return render(request, 'home/help_mp.html', {'users': users})