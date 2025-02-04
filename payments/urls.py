

from django.urls import path
from payments import views

urlpatterns = [
    path('payment_view/', views.payment_view, name='payment_view'),

    path('success/', views.success, name='payment_success'),
    path('failure/', views.failure, name='payment_failure'),
    path('pending/', views.pending, name='payment_pending'),
    
    path('process_payment/', views.process_payment, name='process_payment'),

]