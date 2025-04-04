

from django.urls import path
from users import views


urlpatterns = [
    path('register-user/', views.register_user, name='register_user_page'),
    
    path('profile/', views.profile_page, name='user_profile'),
    
    path('profile/<str:tab_name>/', views.profile_tab, name='profile_tab'),
    
    # Agregados como api forms de admin
    path('upload-to-imgbb/', views.upload_to_imgbb, name='update_header'),
    
]