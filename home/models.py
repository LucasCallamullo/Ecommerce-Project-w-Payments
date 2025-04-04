from django.db import models

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=100)
    logo = models.URLField(blank=True, null=True)
    logo_wsp = models.URLField(blank=True, null=True)

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
    pinterest_url = models.URLField(blank=True, null=True)  # Nueva URL de Pinterest
    image_url = models.URLField(blank=True, null=True)      # URL de la imagen en ImgBB
    main_image = models.BooleanField(default=False)
    soft_delete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Si no hay imágenes existentes, marcar esta como la principal
        if not HeaderImages.objects.filter(store=self.store).exists():
            self.main_image = True  # Solo se establece como principal si no existe ninguna otra imagen

        # Si la imagen es la nueva principal
        elif self.main_image:
            # Si es un nuevo objeto (no tiene id), no necesitamos excluirlo
            if self.id is None:
                HeaderImages.objects.filter(store=self.store).update(main_image=False)
            else:
                # Si es un objeto existente, excluirlo de la actualización
                HeaderImages.objects.filter(store=self.store).exclude(id=self.id).update(main_image=False)
        
        super().save(*args, **kwargs)  # Llamamos al método save después de ejecutar la lógica

    def __str__(self):
        return f"Header Image {self.id}, es Main:{self.main_image}"
    
    class Meta:
        indexes = [
            models.Index(fields=['main_image']),
        ]


class BannerImages(models.Model):
    store = models.ForeignKey('Store', related_name='banners', on_delete=models.CASCADE)
    pinterest_url = models.URLField(blank=True, null=True)  # Nueva URL de Pinterest
    image_url = models.URLField(blank=True, null=True)      # URL de la imagen en ImgBB
    main_image = models.BooleanField(default=False)
    soft_delete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Si no hay imágenes existentes, marcar esta como la principal
        if not BannerImages.objects.filter(store=self.store).exists():
            self.main_image = True  # Solo se establece como principal si no existe ninguna otra imagen

        # Si la imagen es la nueva principal
        elif self.main_image:
            # Si es un nuevo objeto (no tiene id), no necesitamos excluirlo
            if self.id is None:
                BannerImages.objects.filter(store=self.store).update(main_image=False)
            else:
                # Si es un objeto existente, excluirlo de la actualización
                BannerImages.objects.filter(store=self.store).exclude(id=self.id).update(main_image=False)
        
        super().save(*args, **kwargs)  # Llamamos al método save después de ejecutar la lógica

    def __str__(self):
        return f"Banner Image {self.id}, es Main:{self.main_image}"
    
    class Meta:
        indexes = [
            models.Index(fields=['main_image']),
        ]
    