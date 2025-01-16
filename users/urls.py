

from django.urls import path


from users import views

urlpatterns = [
    # filters
    
    # path('images/<int:product_id>/images/', views.get_product_images, name='get_product_images'),
    
    path('register_user/', views.register_user, name='register_user'),
    
    path('register_widget/', views.register_widget, name='register_widget'),
    
    path('close_session/', views.close_session, name='close_session'),
]

