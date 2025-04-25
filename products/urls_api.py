

from django.urls import path
from products.views_api import *


# ==============================================================================
#                        DRF API ENDPOINTS
# ==============================================================================
# NOTE for NAME URL on dtf we use -

urlpatterns = [
    
    # Use query parameters for this ( example = ?available=true&category=1&subcategory=3 )
    path('products-filter/', ProductList.as_view(), name='prod-all-list'),
    
    path('products-search/', ProductUpdateCardsQuery.as_view(), name='prod-search-q'),
    
    # endpoints images 
    path('products-images/<int:product_id>/', ProductImagesView.as_view(), name='prod-images'),


    # url para actualizar productos
    path('api/product/', ProductAPIView.as_view(), name='product-update-api'),
    
    path('api/product/images/delete', ProductImagesView.as_view(), name='product-images-delete-api'),
    path('api/product/images/create', ProductImagesView.as_view(), name='product-images-create-api'),

]