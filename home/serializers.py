

from rest_framework import serializers

from home.models import Store

from rest_framework.exceptions import AuthenticationFailed, ValidationError

from django.core.validators import validate_email
from django.core.exceptions import ValidationError



class UpdateStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            'name', 'address', 'email', 
            'cellphone', 'wsp_number',
            'ig_url', 'fb_url', 'tt_url',
            'tw_url', 'google_url'
        ]
        extra_kwargs = {
            'email': {'validators': [validate_email]},
            
            'name': {'required': False},
            'address': {'required': False},
            'wsp_number': {'required': False},
            'cellphone': {'required': False},
            
            'ig_url': {'required': False},
            'fb_url': {'required': False},
            'tt_url': {'required': False},
            'tw_url': {'required': False},
            'google_url': {'required': False},
        }
