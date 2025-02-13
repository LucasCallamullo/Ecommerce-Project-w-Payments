

from django.urls import path
from favorites.views import ToggleFavoriteProduct


urlpatterns = [
    path('favorites-products/', ToggleFavoriteProduct.as_view(), name='favorites_product'),
]

