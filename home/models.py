from django.db import models

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='ecommerce/logo/', default='ecommerce/default_logo.jpg', 
                            blank=True, null=True)

    ig_url = models.URLField(blank=True, null=True, default="https://www.instagram.com")
    tw_url = models.URLField(blank=True, null=True, default="https://x.com/home")
    fb_url = models.URLField(blank=True, null=True, default="https://www.facebook.com")
    tt_url = models.URLField(blank=True, null=True, default="https://www.tiktok.com")
    google_url = models.URLField(blank=True, null=True)
    wsp_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=180, blank=True, null=True)
    cellphone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class HeaderImages(models.Model):
    store = models.ForeignKey('Store', related_name='headers', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ecommerce/headers/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    main_image = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        # Si no hay imágenes existentes, marcar esta como la principal
        if not HeaderImages.objects.exists():
            self.main_image = True
            
        # Si la imagen es la nueva principal, desmarcar las demás
        elif self.main_image:
            HeaderImages.objects.update(main_header=False)
            self.main_image = True
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Header Image {self.id}, es Main:{self.main_image}"


class BannerImages(models.Model):
    store = models.ForeignKey('Store', related_name='banners', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ecommerce/banners/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    main_image = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Si no hay imágenes existentes, marcar esta como la principal
        if not BannerImages.objects.exists():
            self.main_image = True
            
        # Si la imagen es la nueva principal, desmarcar las demás
        elif self.main_image:
            BannerImages.objects.update(main_banner=False)
            self.main_image = True
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Banner Image {self.id}, es Main:{self.main_image}"
    