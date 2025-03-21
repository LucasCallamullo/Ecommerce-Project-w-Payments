from django.shortcuts import render

# Create your views here.

from users.models import CustomUser
from products.models import Product


def home(request):
    products = Product.objects.select_related('category').all()
    products_by_category = {}
    
    user = request.user
    favorite_product_ids = None
    if user.is_authenticated:
        # IDs de productos favoritos
        favorite_product_ids = set(user.favorites.values_list('product', flat=True)) 

    for product in products:
        category_name = product.category.name
        if category_name not in products_by_category:
            products_by_category[category_name] = []
        products_by_category[category_name].append(product)
        
    context = {
        "favorite_product_ids": favorite_product_ids,
        'products_by_category': products_by_category,
        'products': products
    }

    return render(request, 'home/home.html', context)


def help_mp(request):
    users = CustomUser.objects.filter(is_superuser=False)
    return render(request, 'home/help_mp.html', {'users': users})







