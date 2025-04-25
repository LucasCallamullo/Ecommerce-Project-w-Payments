

from django.urls import path
from dashboard import views

urlpatterns = [
    
    path('main-dashboard/', views.main_dashboard, name='main_dashboard'),
    
    # html response
    path('dashboard/filter/products', views.dash_filter_products, name='dash_filter_products'),
    path('dashboard/sort/products', views.dash_sort_products, name='dash_sort_products'),
    
]
