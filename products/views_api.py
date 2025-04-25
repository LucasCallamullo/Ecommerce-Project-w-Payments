

# ==============================================================================
#                        DRF API VIEWS ENDPOINTS
# ==============================================================================
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny

from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import NotFound

from products.serializers import ProductListFilters, PBrandSerializer

from products.models import Product, PCategory, PSubcategory, PBrand, ProductImage

from products import filters, utils


from django.template.loader import render_to_string
from users.permissions import IsAdminOrSuperUser

# views.py
from products.serializers import ProductSerializer


class ProductAPIView(APIView):
    # 1. Verificar si es role == 'admin' o user.id == 1
    permission_classes = [IsAdminOrSuperUser]
    
    def put(self, request):
        # 2. Validación del formato del ID (evita consulta innecesaria a DB)
        product_id = utils.valid_id_or_None(request.data.get("id"))
        if not product_id:
            return Response({"detail": "ID inválido: debe ser un número positivo"}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Verificación de existencia (consulta a DB sólo si el ID es válido)
        try:
            products = (
                Product.objects.filter(id=product_id)
                .selected_related_w_only(
                    fk_fields=('category', 'subcategory', 'brand'),
                    only_fields=(filters.PRODUCT_FIELDS_UPDATE)
                )
                .prefetch_images_all(ProductImage)
            )

            product = get_object_or_404(products, id=product_id)
            
        except NotFound:
            # lanza status HTTP_404_NOT_FOUND, detail = message para personalizar el mensaje de respuesta
            raise NotFound(detail="No existe un producto con este ID.")
        
        # 4. Pasamos al serializer el objeto, la data/json(body), y actualizacion parcial de campos
        serializer = ProductSerializer(product, data=request.data, partial=True, context={'user': request.user})
        
        # 5. Verifica el formulario sino retorna algunos de los raise serializers.ValidationError
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # 6. aca DRF llama internamente a update(instance, validated_data)
        serializer.save()
        return Response({"success": True}, status=status.HTTP_200_OK)
    

class ProductImagesView(APIView):
    
    # 1 - Sobreescribir metodos para aplicar distintos parsers/permissions segun la peticion http
    def get_parsers(self):
        """If the method is POST, it returns MultiPartParser to allow file uploads
        For (GET, DELETE), it uses the default parsers defined in the base class or DRF settings."""
        if self.request.method == 'POST':
            return [MultiPartParser()]    # Parser para recibir archivos
        return super().get_parsers()
    
    def get_permissions(self):
        """Permisos estrictos para POST/DELETE, abierto para otros"""
        if self.request.method in ('POST', 'DELETE'):
            return [IsAdminOrSuperUser()]    # Permissions custom en user.permissions
        return [AllowAny()]
    
    def post(self, request):
        # 1. Validar datos de entrada
        product_id = utils.valid_id_or_None(request.data.get('id')) 
        if not product_id:
            return Response({"detail": "Se requiere el ID del producto"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Verificación de existencia (consulta a DB sólo si el ID es válido)
        try:
            product = get_object_or_404(Product, id=product_id)
        except NotFound:
            # lanza status HTTP_404_NOT_FOUND, detail = message para personalizar el mensaje de respuesta
            raise NotFound(detail="No existe un producto con este ID.")

        # 3. Procesar imágenes
        uploaded_urls = []
        errors = []
        for img in request.FILES.getlist('images'):
            try:
                utils.validate_image_file(img)  # Validaciones locales primero
                url = utils.get_url_from_imgbb(img)  # Validaciones de ImgBB
                ProductImage.objects.create(product=product, image_url=url)
                uploaded_urls.append(url)
                
            # si get_url_from_imgbb devolviera algun problema lo almacenamos para mostrar despues
            except ValueError as e:
                errors.append(f"{img.name}: {str(e)}")
                continue
            
            except Exception as e:
                errors.append(f"{img.name}: Error inesperado - {str(e)}")
                continue

        # 3. Construir respuesta
        response_data = {
            "success": True if uploaded_urls else False,
            "uploaded_images": uploaded_urls,
            "errors": errors if errors else None,
            "total_uploaded": len(uploaded_urls)
        }

        return Response(response_data, status=status.HTTP_201_CREATED if uploaded_urls else status.HTTP_207_MULTI_STATUS)
        
    def delete(self, request):
        # 2. Validación del formato del ID (evita consulta innecesaria a DB)
        product_id = utils.valid_id_or_None(request.data.get("id"))
        if not product_id:
            return Response({"detail": "ID inválido: debe ser un número positivo"}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Obtener los IDs de las imágenes a eliminar y validarlos
        delete_images = request.data.get("delete_images", [])
        if not delete_images:
            return Response({"detail": "No se especificaron imágenes para eliminar."}, status=status.HTTP_400_BAD_REQUEST)
        
        print("DELETE ENTROAMOS", delete_images, " | ", product_id)
        
        # 4. Filtrar solo los IDs válidos
        valid_image_ids = {int(i) for i in delete_images if utils.valid_id_or_None(i)}
        if not valid_image_ids:
            return Response({"detail": "Ningún ID de imagen válido para eliminar."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 5. Verificación de existencia (consulta a DB sólo si el ID es válido)
        try:
            product = get_object_or_404(
                Product.objects.prefetch_images_all(ProductImage), 
                id=product_id    # ya aplica el filter() aca
            )
        except NotFound:
            # lanza status HTTP_404_NOT_FOUND, detail = message para personalizar el mensaje de respuesta
            raise NotFound(detail="No existe un producto con este ID.")
        
        # 6. Verificar si eliminamos la main
        update_image_url = False
        for image in product.images_all:
            if image.id in valid_image_ids:
                update_image_url = True
                break

        # 7. Eliminar directamente las imágenes que existen y coinciden
        deleted_count, _ = ProductImage.objects.filter(id__in=valid_image_ids, product=product).delete()
        
        # 8. Verificar si eliminamos la main
        if update_image_url:
            for image in product.images_all:
                if image:
                    image.update_main_image()
                    product.update_main_image(image.image_url)
                    break
        
        response_data = {"success": True, "deleted_count": deleted_count}
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get(self, request, product_id):
        
        # 1. Verificación de existencia (consulta a DB sólo si el ID es válido)
        try:
            product = get_object_or_404(
                Product.objects.prefetch_images_all(ProductImage), 
                id=product_id    # ya aplica el filter() aca
            )
            
            # 2. Filtra las imágenes válidas
            images = [image.image_url for image in product.images_all if image.image_url]
            return Response({'images': images})
        
        except NotFound:
            # 3. Lanza un error 404 si no se encuentra el producto
            raise NotFound(detail="No existe un producto con este ID.")








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
        category = filters.get_model_or_None(PCategory, id=category_id)
        subcategory = filters.get_model_or_None(PSubcategory, id=subcategory_id)
        
        # This is for some bad request without category or subcategorys
        if category_id and not category:
            response_data = {'message': f'No se encontraron productos para la category ID: {category_id}'}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
        if subcategory_id and not subcategory:
            response_data = {'message': f'No se encontraron productos para la subcategory ID: {subcategory_id}'}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        # Obtenemos un queryset filtrado par las variables que mandamos
        products = filters.get_products_filters(
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
            
            user = request.user
            favorite_product_ids = None
            if user.is_authenticated:
                # IDs de productos favoritos
                favorite_product_ids = set(user.favorites.values_list('product', flat=True))  
            
            response_data = {
                'message': message,
                'total_products': products.count(),
                'products': product_serializer.data,
                'favorite_product_ids': favorite_product_ids,
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
        category = filters.get_model_or_None(PCategory, category_id)
        subcategory = filters.get_model_or_None(PCategory, subcategory_id)

        products = filters.get_products_filters(
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
        user = request.user
        favorite_product_ids = None
        if user.is_authenticated:
            # IDs de productos favoritos
            favorite_product_ids = set(user.favorites.values_list('product', flat=True)) 
        
        context = {
            'products': products,
            'favorite_product_ids': favorite_product_ids
        }
        html_cards = render_to_string('products/products_list_cards.html', context)
        return Response({'html_cards': html_cards}, status=status.HTTP_200_OK)






