

# ==============================================================================
#                        DRF API VIEWS ENDPOINTS
# ==============================================================================
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from productos.serializers import ProductListFilters, PBrandSerializer
from productos.models import Product, PCategory, PSubcategory, PBrand
from productos import utils
from django.template.loader import render_to_string

# Variable creada parcialmente para controlar el comportamiento de servir todo como api 
# o renderizar algunos html desde el servidor
API_FULL = False


class ProductList(APIView):
    """
    Vista que maneja la solicitud GET para obtener una lista de productos.
    
    Permite filtrar los productos según disponibilidad, categoría y subcategoría 
    a través de los parámetros proporcionados en la URL.
    """
    def get(self, request):
        """
        Maneja la solicitud GET para obtener productos filtrados.
        
        Args:
            request (request): 
                El objeto de solicitud que contiene los parámetros de filtrado.

        Returns:
            Response: 
                productos filtrados, mensaje de depuración, y el total de productos encontrados.
        """
        # Obtener parametros de la url
        available = request.GET.get('available', 'true').lower() == 'true'
        category_id = request.GET.get('category', None)
        subcategory_id = request.GET.get('subcategory', None)
        top_query = request.GET.get('topQuery', None)
        
        # La función valida los datos y devuelve el objeto que corresponda para filtrar despues
        # si no existiera o el request.GET.get is None devolvería None y no afectará al filtrado
        category = utils.get_model_or_None(PCategory, id=category_id)
        subcategory = utils.get_model_or_None(PSubcategory, id=subcategory_id)
        
        # This is for some bad request without category or subcategorys
        if category_id and not category:
            response_data = {'message': f'No se encontraron productos para la category ID: {category_id}'}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
        if subcategory_id and not subcategory:
            response_data = {'message': f'No se encontraron productos para la subcategory ID: {subcategory_id}'}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        # Obtenemos un queryset filtrado par las variables que mandamos
        products = utils.get_products_filters(
            available = available, 
            category = category.id if category else None, 
            subcategory = subcategory.id if subcategory else None,
            top_query = top_query if top_query else None,
        )
        
        # Obtenemos los objetos completos de las marcas asociadas a los productos filtrados
        brands = PBrand.objects.filter(product__in=products).distinct()
        brand_serializer = PBrandSerializer(brands, many=True)
        
        # Si hay productos, serializamos y respondemos con los productos
        if products.exists():
            message = f"Category: {category} | Sub-Category: {subcategory} | Available: {available}"
            product_serializer = ProductListFilters(products, many=True)
            response_data = {
                'message': message,
                'total_products': products.count(),
                'products': product_serializer.data,
                'brands': brand_serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        else:
            # Si no hay productos, respondemos con un mensaje adecuado
            response_data = {
                'message': 'No se encontraron productos',
                'total_products': 0,
                'products': []  # Lista vacía en caso de no haber productos
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


class ProductUpdateCardsQuery(APIView):
    def get(self, request):
        
        # Obtenemos las parametros desde el query
        top_query = request.GET.get('topQuery', None)
        category_id = request.GET.get('categoryId', None)
        subcategory_id = request.GET.get('subCategoryId', None)
        inputNow = request.GET.get('inputNow', None)
        
        # Para normalizar y filtrar espacios extra
        top_query = utils.normalize_or_None(top_query)
        inputNow = utils.normalize_or_None(inputNow)

        # recuperamos el queryset filtrado por los datos que tenemos
        category = utils.get_model_or_None(PCategory, category_id)
        subcategory = utils.get_model_or_None(PCategory, subcategory_id)


        products = utils.get_products_filters(
            category = category.id if category else None, 
            subcategory = subcategory.id if subcategory else None,
            top_query = top_query,
        )
        
        # Filtramos particularmente por el query de la sidebar
        if inputNow:
            # Separar la consulta en palabras individuales
            query_words = inputNow.split()
            # Realizar una búsqueda para cada palabra en el nombre del producto
            for word in query_words:
                products = products.filter(normalized_name__icontains=word)
                
        
        if API_FULL:
            # Si API_FULL es True, devolver los datos en formato JSON usando Response de DRF
            product_serializer = ProductListFilters(products, many=True) 
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        
        # Si API_FULL es False, devolver HTML renderizado
        context = {'products': products}
        html_cards = render_to_string('productos/products_list_cards.html', context)
        return Response({'html_cards': html_cards}, status=status.HTTP_200_OK)


class ProductImagesView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            # Filtra las imágenes válidas
            images = [image.image_url for image in product.images.all() if image.image_url]
            print(images)
            return Response({'images': images})
        
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)



