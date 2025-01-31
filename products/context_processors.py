

from django.core.cache import cache
from products.models import PCategory


def get_categories_n_subcats(request):
    # Tries to get the data from the cache to optimize performance by querying only once
    # instead of doing it every time
    categories_dropmenu = cache.get('categories_dropmenu')
    
    if not categories_dropmenu:
        # Get all categories and prefetch subcategories
        # Prefetch related improves the performance of the query by retrieving all 
        # associated sub-categories at once
        categories = PCategory.objects.prefetch_related('subcategories')
        
        categories_dropmenu = {}
        
        for category in categories:
            # Filter valid subcategories
            subcategories = category.subcategories.all()
            
            # Filter valid subcategories (not None, not empty, not "nan")
            valid_subcategories = [sub for sub in subcategories if sub.name]
            
            # Add the category even if it has no valid subcategories
            categories_dropmenu[category] = valid_subcategories if valid_subcategories else None
                
        # Save the data in the cache for 1 hour (3600 seconds)
        cache.set('categories_dropmenu', categories_dropmenu, 3600)
    
    return {'categories_dropmenu': categories_dropmenu}