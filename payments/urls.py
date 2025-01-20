

from django.urls import path
from payments import views

urlpatterns = [
    path('payment/', views.payment, name='payment'),
]