from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StatusOrder

@admin.register(StatusOrder)
class StatusOrderAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de objetos en el panel de administración
    list_display = ('id', 'name', 'description')

    # Campos que se pueden usar para buscar objetos
    search_fields = ('name', 'description')

    # Campos que se pueden usar para filtrar objetos
    list_filter = ('name',)

    # Campos editables directamente desde la lista de objetos
    list_editable = ('name', 'description')

    # Campos que se pueden usar para ordenar la lista de objetos
    ordering = ('id',)

    # Campos que se mostrarán en el formulario de edición/detalle
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
    )

    # Campos que se mostrarán en el formulario de creación
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'description'),
        }),
    )