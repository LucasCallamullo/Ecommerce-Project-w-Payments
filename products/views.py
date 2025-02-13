

# Create your views here.
from django.shortcuts import render, get_object_or_404
from products.models import Product, PCategory, PSubcategory
from django.http import Http404
from products import utils


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

    # The function validates the data and returns the corresponding object to filter later
    # if it doesn't exist or the request.GET.get is None, it will return None and not affect 
    # the filtering
    category = utils.get_model_or_None(PCategory, slug=cat_slug)
    subcategory = utils.get_model_or_None(PSubcategory, slug=subcat_slug)

    # We get a filtered queryset with all the filtered products
    products = utils.get_products_filters(
        category=category.id if category else None, 
        subcategory=subcategory.id if subcategory else None, 
        empty=True    # Allows us to get an empty queryset
    )
    
    user = request.user
    favorite_product_ids = None
    if user.is_authenticated:
        # IDs de productos favoritos
        favorite_product_ids = set(user.favorites.values_list('product', flat=True)) 

    context = {
        'products': products,
        'category': category,
        'subcategory': subcategory,
        'favorite_product_ids': favorite_product_ids
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
    top_query = utils.normalize_or_None(query) 
    products = utils.get_products_filters(top_query=top_query, empty=True)
    
    user = request.user
    favorite_product_ids = None
    if user.is_authenticated:
        # IDs de productos favoritos
        favorite_product_ids = set(user.favorites.values_list('product', flat=True)) 
        
    context = {
        'products': products,
        'query': query,
        'favorite_product_ids': favorite_product_ids
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
    if not id:
        raise Http404("The product does not exist or the URL is malformed.")
    
    product = get_object_or_404(Product, id=id)
    
    # We get all the necessary data from the product
    category = product.category
    subcategory = product.subcategory
    images_urls = [image.image_url for image in product.images.filter(main_image=False)]
    context = {
        'product': product,
        'main_image_url': product.main_image,
        'images_urls': images_urls,
        'category': category,
        'subcategory': subcategory,
    }
    return render(request, 'products/product_detail.html', context)



from django.db.models import F
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
