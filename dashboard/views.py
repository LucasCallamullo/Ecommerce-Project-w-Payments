

from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Prefetch


from products.models import Product, PBrand, ProductImage
from products.context_processors import get_categories_n_subcats

from products import filters

from users.permissions import admin_or_superuser_required




@admin_or_superuser_required
def dash_sort_products(request):
    context = filters.get_context_filtered_products(request)
    
    # in the future add 'sales'
    sort_by = request.GET.get('sort_by')
    tupla = ('name', 'category__name', 'available', 'updated_at', 'stock', 'price')
    
    # Apply sorting to the product list if a valid field is provided
    if sort_by in tupla:
        sorted_flag = request.GET.get('sorted')
        desc = '-' if sorted_flag == 'desc' else ''
        
        # QuerySet final optimizado el queyset ordenador anterior ordenado
        context["products"] = (
            context["products"].order_by(desc + sort_by).
            selected_related_w_only(
                fk_fields=('category', 'subcategory', 'brand'),
                only_fields=(filters.PRODUCT_FIELDS_DETAIL)
            )
            .prefetch_images_all(ProductImage)
        )
    
    # recuperar las marcas
    brands = PBrand.objects.all().only('name', 'id')
    context["brands"] = brands
    
    # recuperar las categorias
    categories = get_categories_n_subcats(request)
    context["categories_dropmenu"] = categories["categories_dropmenu"]
    
    html = render_to_string("dashboard/table_products.html", context)
    return JsonResponse({"html_section": html})
    
    
@admin_or_superuser_required
def dash_filter_products(request):
    context = filters.get_context_filtered_products(request)
    
    # QuerySet final optimizado el queyset anterior
    context["products"] = (
        context["products"]
        .selected_related_w_only(
            fk_fields=('category', 'subcategory', 'brand'),
            only_fields=(filters.PRODUCT_FIELDS_DETAIL)
        )
        .prefetch_images_all(ProductImage)
    )
    
    # recuperar las marcas
    brands = PBrand.objects.all().only('name', 'id')
    context["brands"] = brands
    
    # recuperar las categorias
    categories = get_categories_n_subcats(request)
    context["categories_dropmenu"] = categories["categories_dropmenu"]
    
    html = render_to_string("dashboard/table_products.html", context)
    return JsonResponse({"html_section": html})


@admin_or_superuser_required
def main_dashboard(request):
    
    # QuerySet optimizado
    products = (
        Product.objects.all()
        .selected_related_w_only(
            fk_fields=('category', 'subcategory', 'brand'),
            only_fields=(filters.PRODUCT_FIELDS_DETAIL)
        )
        .prefetch_images_all(ProductImage)
    )
    
    # recuperar las marcas
    brands = PBrand.objects.all().only('name', 'id')
    
    context = {
        'products': products,
        'brands': brands,
    }
    
    return render(request, "dashboard/dashboard.html", context)