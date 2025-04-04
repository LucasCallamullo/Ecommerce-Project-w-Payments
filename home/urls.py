
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from home import views
from home.views_api import StoreUpdateAPI

urlpatterns = [
    path('', views.home, name='Home'),
    path('help_mp/', views.help_mp, name='help_mp'),
    
    # drf endpoints
    path('api/update-store-info/', StoreUpdateAPI.as_view(), name='update_store_info'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


