from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from productos.models import Product, PCategory, PSubcategory, ProductImage
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse


from django.urls import resolve, reverse

def product_detail(request, id=None, slug=None):
    
    if not id:
        raise Http404("El producto no existe o la URL está mal formada.")
    
    product = get_object_or_404(Product, id=id)
    images_qs = product.images.all()
    
    # Obtener la imagen principal o una de respaldo en caso de que no exista
    main_image = images_qs.filter(main_image=True).first()
    if not main_image:
        main_image = images_qs.first()
    
    context = {
        'product': product,
        'main_image': main_image
    }
    
    return render(request, 'productos/product_detail.html', context)


def get_product_images(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        images = [image.image_url for image in product.images.all() if image.image_url]
        return JsonResponse({'images': images})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    


def product_list(request, cat_slug=None, subcat_slug=None):
    # query = request.GET.get('q')
    productos = Product.objects.all()
    category = None
    subcategory = None
    
    if cat_slug and not subcat_slug:
        category = PCategory.objects.filter(slug=cat_slug).first()
        if category:
            productos = productos.filter(category=category)

    if subcat_slug:
        category = PCategory.objects.filter(slug=cat_slug).first()
        subcategory = PSubcategory.objects.filter(slug=subcat_slug).first()
        if subcategory:
            productos = productos.filter(subcategory=subcategory)

    context = {
        'products': productos,
        'category': category,
        'subcategory': subcategory
    }
    
    return render(request, "productos/products_list.html", context)


def product_top_search(request):

    query = request.GET.get('top_q', '')

    productos = Product.objects.all()
    productos = productos.filter(name__icontains=query)
    
    context = {
        'products': productos,
        'query': query
    }
    
    return render(request, 'productos/products_list.html', context)





def producto_category(request, category_id):
    category = get_object_or_404(PCategory, id=category_id)
    
    productos = Product.objects.filter(category=category).select_related('category')
    
    context = {
        'category': category,
        'products': productos
    }
    
    return render(request, "productos/products_category.html", context)