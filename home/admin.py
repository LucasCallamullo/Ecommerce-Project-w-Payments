from django.contrib import admin

# Register your models here.
from .models import E_HeaderImages, E_BannerImages, Ecommerce


@admin.register(E_HeaderImages)
class E_HeaderImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'main_header', 'image', 'image_url')
    list_filter = ('main_header',)
    actions = ['set_as_main_header']

    def set_as_main_header(self, request, queryset):
        E_HeaderImages.objects.update(main_header=False)
        queryset.update(main_header=True)
    set_as_main_header.short_description = "Set selected as main header"


@admin.register(E_BannerImages)
class E_BannerImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'main_banner', 'image', 'image_url')
    list_filter = ('main_banner',)
    actions = ['set_as_main_banner']

    def set_as_main_banner(self, request, queryset):
        E_BannerImages.objects.update(main_banner=False)
        queryset.update(main_banner=True)
    set_as_main_banner.short_description = "Set selected as main banner"


@admin.register(Ecommerce)
class EcommerceAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo', 'header_image', 'banner_image')
    list_filter = ('name',)

    def has_add_permission(self, request):
        # Permitir agregar solo si no existe ningún modelo Ecommerce
        if Ecommerce.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Evitar eliminar si es el único modelo Ecommerce
        if Ecommerce.objects.count() == 1:
            return False
        return super().has_delete_permission(request, obj)