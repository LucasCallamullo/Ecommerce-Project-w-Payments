from django.db import models

# Create your models here.

""" 
from django.contrib.auth.models import User
from productos.models import Product


class Cart(models.Model):
    usuario = models.ForeignKey('User', on_delete=models.CASCADE, related_name="carrito")
    creado = models.DateTimeField(auto_now_add=True)


class ItemCart(models.Model):
    carrito = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey("Product", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
"""