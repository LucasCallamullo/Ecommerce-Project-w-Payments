

from django.urls import path


from users.views_api import *

urlpatterns = [
    

    
    path('widget-login/', LoginView.as_view(), name='widget-login'),
    path('protected/', ProtectedView.as_view(), name='protected_view'),
    
    
]

