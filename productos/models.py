from django.db import models

# Create your models here.
from django.db.models import UniqueConstraint
from django.utils.text import slugify


class PCategory(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Solo generar slug si 'name' tiene un valor, sino lo guarda como null para futuras consultas
        if self.name: 
            if not self.slug or self.slug == str(self.id):
                self.slug = slugify(self.name)
                # Asegurarse de que el slug sea único
                while PCategory.objects.filter(slug=self.slug).exists():
                    self.slug = slugify(self.name + str(self.id))
        else:
            self.slug = str(self.id)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class PSubcategory(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey('PCategory', on_delete=models.CASCADE, related_name='subcategories')
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Solo generar slug si 'name' tiene un valor, sino lo guarda como null para futuras consultas
        if self.name: 
            if not self.slug or self.slug == str(self.id):
                self.slug = slugify(self.name)
                # Asegurarse de que el slug sea único
                while PSubcategory.objects.filter(slug=self.slug).exists():
                    self.slug = slugify(self.name + str(self.id))
        else:
            self.slug = str(self.id)
        super().save(*args, **kwargs)
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'category'], name='unique_name_per_category')
        ]
    
    def __str__(self):
        return self.name
    

class PBrand(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Solo generar slug si 'name' tiene un valor, sino lo guarda como null para futuras consultas
        if self.name: 
            if not self.slug or self.slug == str(self.id):
                self.slug = slugify(self.name)
                # Asegurarse de que el slug sea único
                while PBrand.objects.filter(slug=self.slug).exists():
                    self.slug = slugify(self.name + str(self.id))
        else:
            self.slug = str(self.id)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    
class ProductImage(models.Model):
    # Tabla relacional adicional muchos a uno para almacenar varias imagenes para los productos
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/product_images/', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    main_image = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Si no hay imágenes existentes, marcar esta como la principal
        if not ProductImage.objects.exists():
            self.main_image = True
            
        elif self.main_image:
            # Si la imagen es la nueva principal, desmarcar las demás
            ProductImage.objects.update(main_image=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.product.name}"
    
    
class Product(models.Model):
    
    # atributos varios del producto
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=False, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True, default=0)
    discount = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    
    # relacion uno a uno, cada producto tiene una categoria, sub, pbrand
    category = models.ForeignKey('PCategory', on_delete=models.CASCADE, blank=True, null=True)
    subcategory = models.ForeignKey('PSubcategory', on_delete=models.CASCADE, blank=True, null=True)
    brand = models.ForeignKey('PBrand', on_delete=models.CASCADE, blank=True, null=True)
    
    # fechas de actualizaciones de losprecios de productos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # para futuras calificaciones de usuarios
    stars = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    
    # para futuros productos que necesiten estos campos como ropa
    # color = models.CharField(max_length=50, null=True, blank=True)
    # size = models.CharField(max_length=50, null=True, blank=True)
    
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Genera el slug a partir del nombre
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        
        # Verificar que la subcategoría pertenece a la categoría seleccionada
        if self.subcategory is not None:
            if self.subcategory.category != self.category:
                raise ValueError(
                    f"La subcategoría '{self.subcategory.name}' no pertenece a la categoría '{self.category.name}'."
                )
        # Llamar al método save original
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    
    @property
    def main_image(self):
        image_url = None
        if self.images.exists():
            images = self.images.all()

            # Intentar obtener la imagen principal
            main_image = images.filter(main_image=True).first()

            # Si no hay una imagen principal, obtener la primera imagen
            image_url = main_image.image_url if main_image else images.first().imagen_url
            
        return image_url
    
        
    