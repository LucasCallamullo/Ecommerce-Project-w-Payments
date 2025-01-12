

from django.urls import path

# from django.conf import settings
# from django.conf.urls.static import static

from productos import views

urlpatterns = [
    # filters
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:cat_slug>/', views.product_list, name='pl_category'),
    path('category/<slug:cat_slug>/<slug:subcat_slug>/', views.product_list, name='pl_subcategory'),
    path('product/<int:id>-<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.product_top_search, name='product_top_search'),
    
    # endpoints images
    path('images/<int:product_id>/images/', views.get_product_images, name='get_product_images'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
