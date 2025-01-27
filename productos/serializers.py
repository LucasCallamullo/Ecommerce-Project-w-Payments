

from rest_framework import serializers
from .models import Product, PCategory, PSubcategory, PBrand, ProductImage



class ProductImageSerializer(serializers.ModelSerializer):
    """Serializador para ProductImage."""
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'main_image']


class PCategorySerializer(serializers.ModelSerializer):
    """Serializador para PCategory."""
    
    class Meta:
        model = PCategory
        fields = ['id', 'name']


class PSubcategorySerializer(serializers.ModelSerializer):
    """Serializador para PSubcategory."""
    
    class Meta:
        model = PSubcategory
        fields = ['id', 'name']


class PBrandSerializer(serializers.ModelSerializer):
    """Serializador para PBrand."""
    
    class Meta:
        model = PBrand
        fields = ['id', 'image', 'image_url']


class ProductListFilters(serializers.ModelSerializer):
    """Serializador para Product."""
    
    # Relaciones explicitas con el Foreign Key
    # brand = PBrandSerializer()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'stock', 'stars', 
            'slug', 'main_image', 'calc_discount'
        ]


