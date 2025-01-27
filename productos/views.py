

# Create your views here.
from django.shortcuts import render, get_object_or_404
from productos.models import Product, PCategory, PSubcategory

from django.http import Http404, JsonResponse
from django.template.loader import render_to_string

from productos import utils


def product_list(request, cat_slug=None, subcat_slug=None):
    """
    Función destinada al renderizado html por filtros de las categorias y subcategorias si 
    las pasamos como parametros

    Args:
        cat_slug (str, optional): Campo Slug de la categoría para filtrar. Defaults to None.
        subcat_slug (str, optional): Campo Slug de la sub-categoría para filtrar.. Defaults to None.
    """
    if not cat_slug and not subcat_slug:
        # En caso de no recibir parametros es porque se llama a la category directa
        products = Product.objects.filter(available=True)
        return render(request, "productos/products_list.html", {'products': products})
    
    # La función valida los datos y devuelve el objeto que corresponda para filtrar despues
    # si no existiera o el request.GET.get is None devolvería None y no afectará al filtrado
    category = utils.get_model_or_None(PCategory, slug=cat_slug)
    subcategory = utils.get_model_or_None(PCategory, slug=subcat_slug)

    # obtenemos un queryset filtrado con todos los productos filtrados
    products = utils.get_products_filters(
        category=category.id if category else None, 
        subcategory=subcategory.id if subcategory else None, 
        empty=True
    )

    context = {
        'products': products,
        'category': category,
        'subcategory': subcategory
    }
    
    return render(request, "productos/products_list.html", context)


def product_top_search(request):
    """
        Función destinada a realizar en filtro de la barra de busqueda superior
        
        # topQuery es el name del input en base.html, casualemente coincide 
        # con la llamada topQuery desde la side bar en product_list.html
    """
    query = request.GET.get('topQuery', '')
    top_query = utils.normalize_or_None(query) # Normalizamos el top query para comparar
    
    # obtenemos un queryset filtrado con todos los productos filtrados
    products = utils.get_products_filters(top_query=top_query, empty=True)
    
    context = {
        'products': products,
        'query': query
    }
    return render(request, 'productos/products_list.html', context)


def product_detail(request, id=None, slug=None):
    """_summary_

    Args:
        id (int, optional): ID del producto para buscar y mostrar su detalle. Defaults to None.
        slug (str, optional): realmente no se utiliza es solo para la url. Defaults to None.

    Raises:
        Http404: Error asignado en caso de no pasar un ID
    """
    if not id:
        raise Http404("El producto no existe o la URL está mal formada.")
    product = get_object_or_404(Product, id=id)
    
    # Obtenemos todos los datos necesarios a partir del producto 
    category = product.category
    subcategory = product.subcategory
    main_image = product.main_image
    images_urls = [image.image_url for image in product.images.filter(main_image=False)]
    context = {
        'product': product,
        'main_image_url': main_image,
        'images_urls': images_urls,
        'category': category,
        'subcategory': subcategory,
    }
    return render(request, 'productos/product_detail.html', context)


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