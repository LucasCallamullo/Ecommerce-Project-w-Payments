

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from products.models import Product, PCategory, PSubcategory
from products import filters, utils
from favorites.utils import get_favs_products

from users.permissions import admin_or_superuser_required

def product_list(request, cat_slug=None, subcat_slug=None):
    """
    Function used for rendering HTML based on filters for categories and subcategories if
    they are passed as parameters.

    Args:
        cat_slug (str, optional): Slug field of the category to filter by. Defaults to None.
        subcat_slug (str, optional): Slug field of the subcategory to filter by. Defaults to None.
    """
    if not cat_slug and not subcat_slug:
        # If no parameters are received, it means the direct category is being called
        products = Product.objects.filter(available=True)
        return render(request, "products/products_list.html", {'products': products})

    # El método `.first()` devuelve el primer objeto que coincide con el filtro o None 
    # si no encuentra ninguno.
    category = PCategory.objects.filter(slug=cat_slug).first() if cat_slug else None
    subcategory = PSubcategory.objects.filter(slug=subcat_slug).first() if subcat_slug else None

    products = filters.get_products_filters({
        'category': category,
        'subcategory': subcategory
    })
    
    # obtener un set de ids para comparacion en template
    favs_products_ids = get_favs_products(request.user)

    context = {
        'products': products,
        'category': category,
        'subcategory': subcategory,
        'favorite_product_ids': favs_products_ids
    }
    
    return render(request, "products/products_list.html", context)


def product_top_search(request):
    """
    Function used to perform filtering on the top search bar.
    
    # topQuery is the name of the input in base.html, coincidentally it matches
    # with the topQuery call from the sidebar in product_list.html
    """
    # We normalize the top query for comparison
    query = request.GET.get('topQuery', '')
    top_query = filters.normalize_or_None(query)

    products = filters.get_products_filters({'query': top_query})
    
    # obtener un set de ids para comparacion en template
    favs_products_ids = get_favs_products(request.user)
        
    context = {
        'products': products,
        'query': query,
        'favorite_product_ids': favs_products_ids
    }
    
    return render(request, 'products/products_list.html', context)


def product_detail(request, id=None, slug=None):
    """
    Args:
        id (int, optional): ID of the product to search and display its detail. Defaults to None.
        slug (str, optional): actually not used, just for the URL. Defaults to None.

    Raises:
        Http404: Error raised if no ID is passed.
    """
    value_id = utils.valid_id_or_None(str(id))
    if not value_id:
        raise Http404("The product does not exist or the URL is malformed.")
    
    product = get_object_or_404(Product.objects.select_related("category", "subcategory"), id=value_id)
    
    # We get all the necessary data from the product
    category = product.category
    subcategory = product.subcategory
    images_urls = [image.image_url for image in product.images.filter(main_image=False)]
    context = {
        'product': product,
        'images_urls': images_urls,
        'category': category,
        'subcategory': subcategory,
    }
    return render(request, 'products/product_detail.html', context)



from django.db.models import F

@admin_or_superuser_required
def reset_stocks(request):
    """
    Reinicia los stocks sumando el stock reservado al stock general para los productos afectados.
    """
    # Actualizar en bloque usando F() para optimizar
    Product.objects.filter(stock_reserved__gt=0).update(
        stock=F('stock') + F('stock_reserved'),
        stock_reserved=0  # Opcional: reinicia el stock reservado si es necesario
    )

    # Mensaje de confirmación para el usuario (si es necesario)
    return render(request, 'home/home.html')
