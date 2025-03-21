from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from favorites.models import FavoriteProduct
from products.models import Product


class ToggleFavoriteProduct(APIView):
    """
    Vista que maneja la solicitud POST para agregar o quitar un producto de los favoritos del usuario.
    """
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        
        user = request.user
        
        if not user.is_authenticated:
            return Response({'detail': 'please login session for save products.'}, status=status.HTTP_401_UNAUTHORIZED)

        product_id = request.data.get('product_id')

        if not product_id:    # stupid check
            return Response({'detail': 'Product ID is required or not found'}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.get(id=product_id)

        # Verifica si el producto ya está marcado como favorito
        favorite_product, created = FavoriteProduct.objects.get_or_create(user=user, product=product)

        if not created:
            # Si ya existe, lo elimina (es decir, lo desmarca como favorito)
            favorite_product.delete()
            return Response({'detail': 'Product removed from favorites'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Product added to favorites'}, status=status.HTTP_200_OK)
