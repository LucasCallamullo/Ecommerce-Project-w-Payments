from django.db import models
from django.db.models import UniqueConstraint
from django.utils.text import slugify


class PCategory(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True, unique=True)
    slug = models.SlugField(max_length=30, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Only generate slug if 'name' has a value, otherwise save it as null for future queries
        if self.name: 
            if not self.slug or self.slug == str(self.id):
                self.slug = slugify(self.name)
                # Ensure the slug is unique
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
        # Only generate slug if 'name' has a value, otherwise save it as null for future queries
        if self.name: 
            if not self.slug or self.slug == str(self.id):
                self.slug = slugify(self.name)
                # Ensure the slug is unique
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
        # Only generate slug if 'name' has a value, otherwise save it as null for future queries
        if self.name: 
            if not self.slug or self.slug == str(self.id):
                self.slug = slugify(self.name)
                # Ensure the slug is unique
                while PBrand.objects.filter(slug=self.slug).exists():
                    self.slug = slugify(self.name + str(self.id))
        else:
            self.slug = str(self.id)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    # Additional many-to-one relationship table to store multiple images for products
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/product_images/', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True, default="https://back.tiendainval.com/backend/admin/backend/web/archivosDelCliente/items/images/20210108100138no_image_product.png")
    main_image = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # If there are no existing images, mark this one as the main one
        if not self.product.images.exists():
            self.main_image = True
            
        # If there are no images marked as main, mark this one
        elif not self.product.images.filter(main_image=True).first():
            self.main_image = True
            
        # If there is already a main image, set this to false
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
    price_list = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available = models.BooleanField(default=False, null=True, blank=True)
    stock = models.PositiveIntegerField(null=True, blank=True, default=0)
    stock_reserved = models.PositiveIntegerField(default=0)
    
    discount = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    
    # One-to-one relationship, each product has a category, subcategory, and brand
    category = models.ForeignKey('PCategory', on_delete=models.CASCADE, blank=True, null=True)
    subcategory = models.ForeignKey('PSubcategory', on_delete=models.CASCADE, blank=True, null=True)
    brand = models.ForeignKey('PBrand', on_delete=models.CASCADE, blank=True, null=True)
    
    # Date fields for product price updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # For future user ratings
    stars = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    
    # For future products that need these fields like clothing
    # color = models.CharField(max_length=50, null=True, blank=True)
    # size = models.CharField(max_length=50, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check that the subcategory belongs to the selected category
        if self.subcategory is not None:
            if self.subcategory.category != self.category:
                raise ValueError(
                    f"The subcategory '{self.subcategory.name}' does not belong to the category '{self.category.name}'."
                )
                
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    def make_stock_reserved(self, quantity):
        """
            Method for products to reserve stock for different payment orders
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
        """
        This property allows us to identify the main image associated with the product, or
        if not, retrieve an associated image or a default one.

        Returns:
            str: URL of an image associated with the product
        """
        
        image_url = None
        if self.images.exists():
            images = self.images.all()
            # Try to get the main image
            main_image = images.filter(main_image=True).first()
            # If there's no main image, get the first image
            image_url = main_image.image_url if main_image else images.first().imagen_url
            
            if not image_url:
                image_url = "https://back.tiendainval.com/backend/admin/backend/web/archivosDelCliente/items/images/20210108100138no_image_product.png"
            
        return image_url
    
    @property
    def calc_discount(self):
        price = self.price
        discount = self.discount
        discount_amount = price * discount / 100
        new_price = price - discount_amount
        return new_price
