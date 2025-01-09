

from django.urls import path

# from django.conf import settings
# from django.conf.urls.static import static

from productos import views

urlpatterns = [
    path('category/<int:category_id>/', views.producto_category, name='producto_category'),
    
    path('products/', views.product_list, name='product_list'),
    path('<slug:cat_slug>/', views.product_list, name='pl_category'),
    path('<slug:cat_slug>/<slug:subcat_slug>/', views.product_list, name='pl_subcategory'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
