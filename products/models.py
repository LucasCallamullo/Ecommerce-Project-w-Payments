

from django.db import models
from django.db.models import UniqueConstraint, Q
from django.utils.text import slugify


class PCategory(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)
    slug = models.SlugField(max_length=32, blank=True, null=True)
    image_url = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically generate a unique slug from 'name' if it's not manually provided
        if self.name:
            if not self.slug:
                base_slug = slugify(self.name)
                slug = base_slug
                counter = 1

                # Ensure uniqueness by appending a counter if necessary
                while PCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                self.slug = slug
        else:
            self.slug = None

        super().save(*args, **kwargs)

    class Meta:
        # Adds an index only for non-null slug values to optimize lookups
        indexes = [
            models.Index(
                fields=['slug'],
                name='idx_slug_not_null',
                condition=Q(slug__isnull=False)
            )
        ]

        # Enforces uniqueness for non-null slugs at the database level
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_non_null_slug',
                condition=Q(slug__isnull=False)
            )
        ]

    def __str__(self):
        return self.name
    

class PSubcategory(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey('PCategory', on_delete=models.CASCADE, related_name='subcategories')
    slug = models.SlugField(max_length=50, blank=True, null=True)
    image_url = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-generate a unique slug from name if not manually provided
        if self.name and not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            # Ensure slug is unique (ignore current instance)
            while PSubcategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        else:
            self.slug = None

        super().save(*args, **kwargs)

    class Meta:
        # Enforce unique 'name' within a category (allows same name in different categories)
        constraints = [
            UniqueConstraint(
                fields=['name', 'category'],
                name='unique_name_per_category'
            ),
            # Ensure unique non-null slugs (nulls can be duplicated)
            UniqueConstraint(
                fields=['slug'],
                name='unique_non_null_slug_subcat',
                condition=Q(slug__isnull=False)
            )
        ]
        # Optional index to optimize lookups on non-null slugs
        indexes = [
            models.Index(
                fields=['slug'],
                name='idx_slug_not_null_subcat',
                condition=Q(slug__isnull=False)
            )
        ]

    def __str__(self):
        return self.name
    

class PBrand(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)
    slug = models.SlugField(max_length=32, blank=True, null=True)
    image_url = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-generate slug only if 'name' exists and 'slug' is not set
        if self.name:
            if not self.slug:
                base_slug = slugify(self.name)
                slug = base_slug
                counter = 1

                # Ensure the slug is unique (exclude the current instance)
                while PBrand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                self.slug = slug
        else:
            self.slug = None

        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            # Unique constraint for non-null slugs
            UniqueConstraint(
                fields=['slug'],
                name='unique_non_null_slug_brand',
                condition=Q(slug__isnull=False)
            )
        ]
        indexes = [
            # Optional index for performance on non-null slugs
            models.Index(
                fields=['slug'],
                name='idx_slug_not_null_brand',
                condition=Q(slug__isnull=False)
            )
        ]

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    """
    Represents an image associated with a product.
    Multiple images can be linked to the same product,
    but only one is marked as the main image.
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images', help_text="The product this image belongs to.")
    image_url = models.URLField(null=True, blank=True, help_text="URL of the image.")
    main_image = models.BooleanField(default=False, help_text="Main image of a product.")
    
    def update_main_image(self, queryset=None):
        """ 
        Marks this image as the main image and updates the rest as not main.
        
        Args:
            queryset (QuerySet[ProductImage], optional): Prefetched queryset of images belonging 
            to the same product. If provided, it avoids extra DB queries when unsetting other 
            main images.
        """
        if queryset is not None:
            other_ids = [img.id for img in queryset if img.id != self.id]
            if other_ids:
                ProductImage.objects.filter(id__in=other_ids).update(main_image=False)

        self.main_image = True
        self.save(update_fields=['main_image'])
        

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to ensure:
        - The first image added to a product is set as the main image.
        - If this image is marked as main, unmark all others.
        - If no other image is marked as main, this one becomes the main image.
        """
        is_new = self.pk is None
        
        # If it's the first image for the product, set it as main and save it in Product Model
        if is_new:
            # If no image is currently marked as main, mark this one
            product_images = self.product.images.all()

            # Si no hay otra imagen marcada como principal, esta se marca como main
            if not product_images.filter(main_image=True).exists():
                self.main_image = True

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Overrides the default delete method to:
        - Assign a new main image from the remaining ones if this was the main.
        - Update the product's main_image_url field accordingly.
        """
        is_main = self.main_image
        product = self.product if is_main else None
        super().delete(*args, **kwargs)   

        if product:
            new_main = product.images.first()
            if new_main:
                new_main.update_main_image()
                product.update_main_image(new_main.image_url)
            
    def __str__(self):
        return f"Url: {self.image_url} | Product ID: {self.product_id}"
    
    
    # Clear main_image_url if no images left in the product its not really necesary mayve
            # else:
            #    product.main_image = None
            #    product.save(update_fields=["main_image"])


from products.filters import OptimizedQuerySet
class Product(models.Model):
    # For future user ratings
    # stars = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    
    # For future products that need these fields like clothing
    # color = models.CharField(max_length=50, null=True, blank=True)
    # size = models.CharField(max_length=50, null=True, blank=True)
    
    # Esto es para exetnder el modelo de producto y reutilizar filters directos en los queryset Products.objects. methods()
    objects = OptimizedQuerySet.as_manager()
    
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
    main_image = models.URLField(null=True, blank=True)    # asociar una url main, para evitar consultas
    
    # One-to-one relationship, each product has a category, subcategory, and brand
    category = models.ForeignKey('PCategory', on_delete=models.SET_NULL, blank=True, null=True)
    subcategory = models.ForeignKey('PSubcategory', on_delete=models.SET_NULL, blank=True, null=True)
    brand = models.ForeignKey('PBrand', on_delete=models.SET_NULL, blank=True, null=True)

    # Date fields for product price updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
            return self.name
        
    def update_main_image(self, url= None):
        self.main_image = url
        self.save(update_fields=['main_image'])
        
        
    def make_stock_reserved(self, quantity):
        """ Method for products to reserve stock for different payment orders """
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
    def calc_discount(self):
        """
        Calculate the price of the product after applying the discount percentage.

        Returns:
            float: The final price after discount.
        """
        return round(float(self.price) * (1 - float(self.discount) / 100), 2)
    
    
