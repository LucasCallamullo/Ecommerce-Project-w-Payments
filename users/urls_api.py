

from django.urls import path


from users.views_api import *

urlpatterns = [
    
    path('widget-login/', LoginView.as_view(), name='widget_login'),
    
    path('close-session/', CloseView.as_view(), name='close_session'),
    
    path('register-session/', RegisterUserView.as_view(), name='register_user'),
    
    path('user-edit-role/', UserRoleEditView.as_view(), name='user_edit_role'),
    
]

