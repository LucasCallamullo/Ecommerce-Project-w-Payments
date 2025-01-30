

# Create your models here.
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.text import slugify


class PCategory(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True, unique=True)
    slug = models.SlugField(max_length=30, unique=True, blank=True, null=True)

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
    name = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey('PCategory', on_delete=models.CASCADE, related_name='subcategories')
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)

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
    name = models.CharField(max_length=30, blank=True, null=True, unique=True)
    slug = models.SlugField(max_length=30, unique=True, blank=True, null=True)
    
    image = models.ImageField(upload_to='media/brands_logo/', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

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
    image_url = models.URLField(null=True, blank=True, default="https://back.tiendainval.com/backend/admin/backend/web/archivosDelCliente/items/images/20210108100138no_image_product.png")
    main_image = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Si no hay imágenes existentes, marcar esta como la principal
        if not self.product.images.exists():
            self.main_image = True
            
        # Si no hay imágenes del producto marcadas como principal, marcar esta
        elif not self.product.images.filter(main_image=True).first():
            self.main_image = True
            
        # si ya hay imagen principal dar valor de false
        else:
            self.main_image = False
            
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Image for {self.product.name}"
    
    
class Product(models.Model):
    
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    normalized_name = models.CharField(max_length=120, blank=True, null=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=False, null=True, blank=True)
    stock = models.PositiveIntegerField(null=True, blank=True, default=0)
    stock_reserved = models.PositiveIntegerField(default=0)
    
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
    
    def save(self, *args, **kwargs):
        # Verificar que la subcategoría pertenece a la categoría seleccionada
        if self.subcategory is not None:
            if self.subcategory.category != self.category:
                raise ValueError(
                    f"La subcategoría '{self.subcategory.name}' no pertenece a la categoría '{self.category.name}'."
                )
                
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    def make_stock_reserved(self, quantity):
        """
            Metodo de los productos para poder reservar stock en las distintas ordenes de pago
        """
        if not self.available or self.stock < quantity:
            return False
        
        self.stock -= quantity
        self.stock_reserved += quantity
        self.save()
        return True
    
    def make_stock_unreserved(self, quantity):
        self.stock += quantity
        self.stock_reserved -= quantity
        self.save()
        
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
    
    @property
    def calc_discount(self):
        price = self.price
        discount = self.discount
        discount_amount = price * discount / 100
        new_price = price - discount_amount
        return new_price
    