

from products.models import Product

# ============================================================================ 
#                       Filter product stuff
# ============================================================================ 
def get_products_filters(available=True, category=None, subcategory=None, top_query=None, empty=False):
    """
    Filters products based on the provided parameters.
    
    Args:
        available (bool, optional): 
            Filters the initial queryset based on availability. Defaults to True.
        category (ID PCategory, optional): 
            Object used for optional filtering if it exists. Defaults to None.
        subcategory (ID PSubcategory, optional): 
            Object used for optional filtering if it exists. Defaults to None.
        top_query (str, optional):
            Search query that comes from the top search bar.
        empty (bool, optional): 
            Indicates whether an empty queryset can be returned if no filters are passed 
            correctly as parameters.
        
    Return:
        QuerySet Product: Filtered products if there are matches or an empty queryset.
    """
    # Filter products by availability
    products = Product.objects.filter(available=available) if available else Product.objects.all()
    
    # If there's no category, subcategory, and no top_query, return an empty queryset
    if empty and not category and not top_query and not subcategory:
        return Product.objects.none()
    
    if category: 
        products = products.filter(category=category)
        
    if subcategory:
        products = products.filter(subcategory=subcategory)
            
    if top_query:
        # Split the query into individual words
        query_words = top_query.split()

        # Perform a search for each word in the product name
        for word in query_words:
            products = products.filter(normalized_name__icontains=word)
    
    return products


def get_model_or_None(object_model, id=None, slug=None):
    """
        Retrieves a model from the database by its ID, if the ID is valid.

    Args:
        object_model (object): 
            The database model from which to get the object
            
        id (str, optional): 
            The ID of the object to search for.
            
        slug (str, optional):
            The slug of the object to search for.

    Returns:
        object: The model if found, otherwise returns None.
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
    # Check if the text is None or empty
    if not text:
        return None
    
    # Replace plus signs '+' with spaces
    text = text.replace('+', ' ')
    
    # Remove accents
    text_without_accents = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

    # Remove special characters
    text_normalized = re.sub(r'[^\w\s]', '', text_without_accents).strip()

    # Reduce multiple spaces to a single one
    text_normalized = re.sub(r'\s+', ' ', text_normalized)

    return text_normalized
