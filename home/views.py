from django.shortcuts import render

# Create your views here.

from users.models import CustomUser
from products.models import Product


from home.models import Store, HeaderImages, BannerImages
from django.db.models import Prefetch


def home(request):
    # Obtener el store con prefetch optimizado
    store = Store.objects.prefetch_related(
        Prefetch('headers', 
            queryset=HeaderImages.objects.filter(soft_delete=False)
            .order_by('-main_image'),
            to_attr='active_headers'
        ),
        Prefetch('banners',
            queryset=BannerImages.objects.filter(soft_delete=False)
            .order_by('-main_image'),
            to_attr='active_banners'
        ),
    ).filter(id=1).first()
    
    products = Product.objects.select_related('category').all()
    products_by_category = {}
    
    user = request.user
    favorite_product_ids = None
    if user.is_authenticated:
        # IDs de productos favoritos
        favorite_product_ids = set(user.favorites.values_list('product', flat=True)) 

    for product in products:
        if not product.category:
            continue
        
        category_name = product.category.name
        if category_name not in products_by_category:
            products_by_category[category_name] = []
        products_by_category[category_name].append(product)
        
    context = {
        'headers_active': store.active_headers,  
        'banners_active': store.active_banners,
        
        "favorite_product_ids": favorite_product_ids,
        'products_by_category': products_by_category,
        'products': products
    }

    return render(request, 'home/home.html', context)


def help_mp(request):
    users = CustomUser.objects.filter(is_superuser=False)
    return render(request, 'home/help_mp.html', {'users': users})







