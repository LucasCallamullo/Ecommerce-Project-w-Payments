

from django.urls import path
from orders import views


urlpatterns = [
    path('order/', views.order, name='order'),
    
    path('extra_form_ajax/', views.extra_form_ajax, name='extra_form_ajax'),
]