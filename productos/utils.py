

from productos.models import Product


# ============================================================================
#                       Filter product stuff
# ============================================================================
def get_products_filters(available=True, category=None, subcategory=None, top_query=None, empty=False):
    """
    Filtra los productos según los parámetros proporcionados.
    
    Args:
        available (bool, optional): 
            Obtiene el queryset inicial según la disponibilidad. Defaults to True.
        category (ID PCategory, optional): 
            Objeto utilizado para filtrar opcionalmente en caso de existir. Defaults to None.
        subcategory (ID PSubcategory, optional): 
            Objeto utilizado para filtrar opcionalmente en caso de existir. Defaults to None.   
        empty (bool, optional): 
            Nos sirve para indicar que podemos devolver un queryset vacío en caso de no tener 
            filtros pasados correctamente como parámetro.
        top_query(str, optional):
            Query search que viene desde la barra de búsqueda superior.
    Return:
        QuerySet Product: Products filtrados si hubiera coincidencias o queryset vacío.
    """
    # Filtrar productos por disponibilidad
    products = Product.objects.filter(available=available) if available else Product.objects.all()
    
    # Si no hay categoría, subcategoría y no hay top_query, devolver queryset vacío
    if empty and not category and not top_query:
        return Product.objects.none()
    
    # Filtrar por categoría si existe
    if category: 
        products = products.filter(category=category)
        
    # Filtrar por subcategoría si existe
    if subcategory:
        products = products.filter(subcategory=subcategory)
            
    # Filtrar por consulta de búsqueda (top_query)
    if top_query:
        # Separar la consulta en palabras individuales
        query_words = top_query.split()

        # Realizar una búsqueda para cada palabra en el nombre del producto
        for word in query_words:
            products = products.filter(normalized_name__icontains=word)
    
    return products


def get_model_or_None(object_model, id=None, slug=None):
    """
        Obtiene un modelo de la base de datos según su ID, si el ID es válido.

    Args:
        object_model (object): 
            El modelo de la db del cual obtener el objeto
            
        id (str, optional): 
            El ID del objeto que se busca.
            
        slug (str, optional):
            El slug del objeto a buscar

    Returns:
        object: el modelo si se encuentra, de lo contrario, return None.
    """
    if not id and not slug:
        return None
    
    try:
        if id and str(id).isdigit():
            return object_model.objects.get(id=id)
        
        if slug:
            return object_model.objects.get(slug=slug)

    except object_model.DoesNotExist:
        return None
    
    
import unicodedata
import re
def normalize_or_None(text):
    # Verificamos si el texto es None o vacío
    if not text:
        return None
    
    # Reemplazamos los signos de adición '+' por espacios
    text = text.replace('+', ' ')
    
    # Eliminar acentos
    text_without_accents = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

    # Eliminar caracteres especiales
    text_normalized = re.sub(r'[^\w\s]', '', text_without_accents).strip()

    # Reducir múltiples espacios a uno solo
    text_normalized = re.sub(r'\s+', ' ', text_normalized)

    return text_normalized