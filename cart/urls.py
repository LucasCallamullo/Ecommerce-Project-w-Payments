from django.urls import path
from cart import views

# endpoint para realizar los cambios del carrito dinamicamente en la pagina
urlpatterns = [

    path('carrito/update/', views.update_productos, name='update_productos'),
    path('ver-carrito/', views.cart_page_detail, name='cart_page_detail'),
]