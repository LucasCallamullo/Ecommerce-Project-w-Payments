from django.db import models

# Create your models here.
class Ecommerce(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='ecommerce/logo/', default='ecommerce/default_logo.jpg')
    header_image = models.ForeignKey('E_HeaderImages', on_delete=models.CASCADE, related_name='ecommerce_header', blank=True, null=True)
    banner_image = models.ForeignKey('E_BannerImages', on_delete=models.CASCADE, related_name='ecommerce_banner', blank=True, null=True)

    ig_url = models.URLField(blank=True, null=True, default="https://www.instagram.com")
    tw_url = models.URLField(blank=True, null=True, default="https://x.com/home")
    fb_url = models.URLField(blank=True, null=True, default="https://www.facebook.com")
    tt_url = models.URLField(blank=True, null=True, default="https://www.tiktok.com")
    google_url = models.URLField(blank=True, null=True)
    wsp_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    cellphone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class E_HeaderImages(models.Model):
    image = models.ImageField(upload_to='ecommerce/headers/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    main_header = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.main_header:
            E_HeaderImages.objects.filter(main_header=True).update(main_header=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Header Image {self.id}"


class E_BannerImages(models.Model):
    image = models.ImageField(upload_to='ecommerce/banners/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    main_banner = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.main_banner:
            E_BannerImages.objects.filter(main_banner=True).update(main_banner=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Banner Image {self.id}"

    

    