from django.db import models

# Create your models here.
from django.db.models import UniqueConstraint


class PCategory(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    
    def __str__(self):
        return self.name
    

class PSubcategory(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey('PCategory', on_delete=models.CASCADE, related_name='subcategories')
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'category'], name='unique_name_per_category')
        ]
    
    def __str__(self):
        return self.name
    

class PBrand(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    
    def __str__(self):
        return self.name
    
    
class ProductImage(models.Model):
    # Tabla relacional adicional muchos a uno para almacenar varias imagenes para los productos
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/product_images/', null=True, blank=True)
    image_url = models.URLField(default="https://i.pinimg.com/736x/74/fe/76/74fe76b1b09e521dd7bcdf8dd89ba026.jpg",
                                null=True, blank=True)
    main_image = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"
    
    
class Product(models.Model):
    
    # atributos varios del producto
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=False)
    stock = models.IntegerField(null=True, blank=True, default=0)
    discount = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    
    # relacion uno a uno, cada producto tiene una categoria, sub, pbrand
    category = models.ForeignKey('PCategory', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('PSubcategory', on_delete=models.CASCADE)
    brand = models.ForeignKey('PBrand', on_delete=models.CASCADE)
    
    # fechas de actualizaciones de losprecios de productos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # para futuras calificaciones de usuarios
    stars = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    
    # para futuros productos que necesiten estos campos como ropa
    # color = models.CharField(max_length=50, null=True, blank=True)
    # size = models.CharField(max_length=50, null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        # Verificar que la subcategoría pertenece a la categoría seleccionada
        if self.subcategory.category != self.category:
            raise ValueError(
                f"La subcategoría '{self.subcategory.name}' no pertenece a la categoría '{self.category.name}'."
            )
        # Llamar al método save original
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    