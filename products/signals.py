

""" 
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from products.models import ProductImage

@receiver(post_save, sender=ProductImage)
def refresh_main_image_on_save(sender, instance, **kwargs):
    # Product = instance.product, Is Main Saved ? instance.main_image , get url instance.image_url   
    if instance.main_image: 
        # instance.product.update_main_image_url(instance.image_url)
"""