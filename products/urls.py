

from django.urls import path
from products import views

# =======================================================================
#      Views DJANGO renderizado incial de paginas desde el servidor
# =======================================================================
urlpatterns = [
    path('reset_stocks/', views.reset_stocks, name='reset_stocks'),
    
    # filters to product_list.html
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:cat_slug>/', views.product_list, name='pl_category'),
    path('category/<slug:cat_slug>/<slug:subcat_slug>/', views.product_list, name='pl_subcategory'),
    path('product/search/', views.product_top_search, name='product_top_search'),
   
    # url for product_detail.html
    path('product/25<int:id>-<slug:slug>/', views.product_detail, name='product_detail'),
]

# from django.conf import settings
# from django.conf.urls.static import static
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 