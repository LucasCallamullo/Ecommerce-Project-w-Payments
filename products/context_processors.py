
from django.core.cache import cache
from products.models import PCategory


def get_categories_n_subcats(request):
    # Intenta obtener los datos del caché, para optimizar el rendimiento realizando la consulta una vez
    # en vez de realizarlo cada vez
    categories_dropmenu = cache.get('categories_dropmenu')
    
    if not categories_dropmenu:
        # Obtener todas las categorías y prefetch de subcategorías
        # Prefetch related aumenta el rendimiento de la consulta obteniendo de una vez todas 
        # las sub-categories asociadas de una vez
        categories = PCategory.objects.prefetch_related('subcategories')
        
        categories_dropmenu = {}
        
        for category in categories:
            # Filtrar subcategorías válidas
            subcategories = category.subcategories.all()
            
            # Filtrar subcategorías válidas (no None, no vacías, no "nan")
            valid_subcategories = [sub for sub in subcategories if sub.name]
            
            # Agregar la categoría incluso si no tiene subcategorías válidas
            categories_dropmenu[category] = valid_subcategories if valid_subcategories else None
                
        # Guarda los datos en caché por 1 hora (3600 segundos)
        cache.set('categories_dropmenu', categories_dropmenu, 3600)
    
    return {'categories_dropmenu': categories_dropmenu}
