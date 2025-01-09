from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from productos.models import Product, PCategory, PSubcategory, ProductImage
from django.shortcuts import get_object_or_404

def product_list(request, cat_slug=None, subcat_slug=None):
    # query = request.GET.get('q')

    productos = Product.objects.all()

    if cat_slug and not subcat_slug:
        category = PCategory.objects.filter(slug=cat_slug).first()
        if category:
            productos = productos.filter(category=category)

    if subcat_slug:
        subcategory = PSubcategory.objects.filter(slug=subcat_slug).first()
        if subcategory:
            productos = productos.filter(subcategory=subcategory)

    # if query:
    #    productos = productos.filter(name__icontains=query)

    context = {
        'products': productos,
        'category': PCategory.objects.filter(slug=cat_slug).first(),
        'subcategory': PSubcategory.objects.filter(slug=subcat_slug).first()
        # 'query': query
    }
    
    return render(request, "productos/products_list.html", context)



def producto_category(request, category_id):
    category = get_object_or_404(PCategory, id=category_id)
    
    productos = Product.objects.filter(category=category).select_related('category')
    
    context = {
        'category': category,
        'products': productos
    }
    
    return render(request, "productos/products_category.html", context)