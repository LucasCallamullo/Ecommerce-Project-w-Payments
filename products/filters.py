



from django.db import models
from django.db.models import Q, Prefetch
from products import utils

# CONST TUPLES FILTERS
# para desempaquetar la tupla como argumentos para .only().
PRODUCT_FIELDS_UPDATE = (
    'name', 'slug', 'normalized_name', 'price', 'price_list', 'available', 'stock',
    'description', 'discount', 'updated_at', 'main_image',
    'subcategory__id', 'subcategory__name',
    'category__id', 'category__name', 
    'brand__id', 'brand__name'
)

PRODUCT_FIELDS_DETAIL = (
    'name', 'price', 'price_list', 'available', 'stock',
    'description', 'discount', 'updated_at', 'main_image',
    'subcategory__id', 'subcategory__name',
    'category__id', 'category__name', 
    'brand__id', 'brand__name'
)


class OptimizedQuerySet(models.QuerySet):
    
    def selected_related_w_only(self: models.QuerySet, fk_fields: tuple= None, only_fields: tuple= None):
        """ 
        Encadenamiento de methodos 'Django Styles' --> Ejemplo de uso:
        products = (
            Product.objects
            .all()  # Opcional: .filter(...) si necesitas filtros base
            .selected_related_w_only(
                fk_fields=('category', 'subcategory', 'brand'),
                only_fields=('id', 'name', 'category__name', ...)
            )
            .prefetch_images_all(model_image)
        )
        """
        if fk_fields:
            self = self.select_related(*fk_fields)
        if only_fields:
            self = self.only(*only_fields)
        return self

    def prefetch_images_all(self: models.QuerySet, model_images: object):
        """ obtiene un modelo de imagenes asociado de muchos a uno ejemplo "ProductImage" """
        return self.prefetch_related(
            Prefetch(
                'images',
                queryset=model_images.objects.only('id', 'image_url', 'main_image'),
                to_attr='images_all'
            )
        )
    

def get_context_filtered_products(request):
    from products.models import PCategory, PSubcategory    # evita importacion ciclica
    
    """
    Extracts and validates filter parameters from the GET request, retrieves the filtered 
    list of products, and builds a context dictionary with relevant data for rendering.

    Parameters:
        request (HttpRequest): The incoming HTTP request containing GET parameters.

    Returns:
        dict: A context dictionary containing the following keys:
            - "products" (QuerySet): The filtered list of Product objects based on the parameters.
            - "category" (PCategory or None): The selected category object, or None if not found.
            - "subcategory" (PSubcategory or None): The selected subcategory object, or None if not found.
            - "available" (str): Availability filter value as a string ('0', '1', or '2'). Defaults to '1'.
                - '0' = only unavailable products
                - '1' = only available products
                - '2' = all products (available and unavailable)
            - "query" (str or None): The search query string, if any, used to filter products by name or other fields.
    """
    cat_id = utils.valid_id_or_None(request.GET.get('category')) 
    subcat_id = utils.valid_id_or_None(request.GET.get('subcategory'))
    query = request.GET.get('query')

    # Forzar que solo sea '0', '1' o '2', si no es válido, usar '1'
    available = request.GET.get('available')
    available = available if available in ('0', '1', '2') else '1'

    category = PCategory.objects.filter(id=cat_id).first() if cat_id else None
    subcategory = PSubcategory.objects.filter(id=subcat_id).first() if subcat_id else None

    products = get_products_filters({
        'category': category,
        'subcategory': subcategory,
        'query': query,
        'available': True if available == '1' else False, 
        'get_all': True if available == '2' else False
    })

    return {
        "products": products,
        "category": category,
        "subcategory": subcategory,
        "available": available,
        "query": query,
    }


def get_products_filters(filters: dict):
    from products.models import Product
    """
    Filters products based on provided dictionary filters.
    
    Args:
        filters (dict): Dictionary with optional keys:
            - 'available' (bool)
            - 'category' (ID or instance)
            - 'subcategory' (ID or instance)
            - 'query' (str)
            - 'get_all' (bool): If True, returns all products regardless of 'available'.
        
    Returns:
        QuerySet[Product]: Filtered queryset (may be empty if no matches).
    """
    get_all = filters.get('get_all', False)   # if u want different value
    available = filters.get('available', True)   # if u want different value
    category = filters.get('category')           # <- default: None
    subcategory = filters.get('subcategory')     # <- default: None
    query = filters.get('query')                 # <- default: None

    # Si all está activo, no se filtra por disponibilidad
    products = Product.objects.all() if get_all else Product.objects.filter(available=available)

    if category:
        products = products.filter(category=category)

    if subcategory:
        products = products.filter(subcategory=subcategory)

    if query:
        # 1. Creamos una lista de condiciones Q (consultas) para cada palabra en la búsqueda:
        queries = [Q(normalized_name__icontains=word) for word in query.split()]

        # 2. Extraemos la última condición Q de la lista para usarla como base:
        query_filter = queries.pop()

        # 3. Combinamos todas las condiciones Q restantes usando OR (|):
        #    - Recorremos las condiciones Q que quedaron en la lista
        #    - El operador |= va "sumando" condiciones con OR lógico
        #    - Ejemplo: query_filter = (Q por 'zapatilla') | (Q por 'nike')
        for q in queries:
            query_filter |= q

        # 4. Aplicamos el filtro combinado al queryset de productos:
        #    - La consulta SQL resultante tendrá una cláusula WHERE con múltiples LIKE unidos por OR
        #    - Ejemplo: WHERE normalized_name LIKE '%zapatilla%' OR normalized_name LIKE '%nike%'
        products = products.filter(query_filter)

    return products

