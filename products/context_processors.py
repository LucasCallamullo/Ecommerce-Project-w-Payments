

from django.core.cache import cache
from products.models import PCategory


def get_categories_n_subcats(request):
    # Tries to get the data from the cache to optimize performance by querying only once
    # instead of doing it every time
    categories_dropmenu = cache.get('categories_dropmenu')
    
    if not categories_dropmenu:
        # Obtén las categorías junto con las subcategorías que necesitas (con los campos que te interesan)
        categories = ( 
            PCategory.objects
            .prefetch_related('subcategories')
            .only('id', 'name', 'slug', 'subcategories__id', 'subcategories__name', 'subcategories__slug')
        )

        categories_dropmenu = {}
        for category in categories:
            # Obtenemos las subcategorías de cada categoría con los campos necesarios
            valid_subcategories = [sub for sub in category.subcategories.all() if sub.name]
            
            # Asignamos las subcategorías válidas a la categoría (si no hay, asignamos None)
            categories_dropmenu[category] = valid_subcategories if valid_subcategories else None
                
        # Save the data in the cache for 1 hour (3600 seconds)
        cache.set('categories_dropmenu', categories_dropmenu, 3600)
    
    return {'categories_dropmenu': categories_dropmenu}