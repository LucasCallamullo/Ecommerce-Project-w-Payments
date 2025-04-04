

from django.urls import path
from orders.views_api import * 



urlpatterns = [
    
    path("order-form/", order_form.as_view(), name="valid_order_form"),
    
    
    path("edit-shipment/", EditShipmentView.as_view(), name="edit_shipments"),
    
    path("edit-payment/", EditPaymentView.as_view(), name="edit_payments"),
]

