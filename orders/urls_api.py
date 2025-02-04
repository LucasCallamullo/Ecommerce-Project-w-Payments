

from django.urls import path
from orders.views_api import * 



urlpatterns = [
    path("order-form/", order_form.as_view(), name="valid_order_form")
]

