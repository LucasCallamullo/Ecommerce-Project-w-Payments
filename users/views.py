

# Create your views here.
from django.shortcuts import render, redirect

from products.models import Product
from favorites.models import FavoriteProduct
from orders.models import Order

# admins forms
from django.template.loader import render_to_string
from django.http import JsonResponse

from home.models import Store, HeaderImages, BannerImages
from users import utils

PROVINCIAS_CHOICES = [
    ('', 'Selecciona una provincia'),
    ('Buenos Aires', 'Buenos Aires'),
    ('Catamarca', 'Catamarca'),
    ('Chaco', 'Chaco'),
    ('Chubut', 'Chubut'),
    ('CABA', 'Ciudad Autónoma de Buenos Aires'),
    ('Córdoba', 'Córdoba'),
    ('Corrientes', 'Corrientes'),
    ('Entre Ríos', 'Entre Ríos'),
    ('Formosa', 'Formosa'),
    ('Jujuy', 'Jujuy'),
    ('La Pampa', 'La Pampa'),
    ('La Rioja', 'La Rioja'),
    ('Mendoza', 'Mendoza'),
    ('Misiones', 'Misiones'),
    ('Neuquén', 'Neuquén'),
    ('Río Negro', 'Río Negro'),
    ('Salta', 'Salta'),
    ('San Juan', 'San Juan'),
    ('San Luis', 'San Luis'),
    ('Santa Cruz', 'Santa Cruz'),
    ('Santa Fe', 'Santa Fe'),
    ('Santiago del Estero', 'Santiago del Estero'),
    ('Tierra del Fuego', 'Tierra del Fuego'),
    ('Tucumán', 'Tucumán')
]


def upload_to_imgbb(request):
    
    if request.method == "POST":
        if request.user.id != 1 or request.user.role != 'admin':
            return JsonResponse({"success": "no se que haces con este endpoint.."})
        
        action = request.POST.get("action_name")  # "edit" o "delete"
        soft_delete = request.POST.get("soft_delete", "false") == "true"
        main_image = request.POST.get("main_image", "false") == "true"
        obj_name = request.POST.get("obj_name")
        obj_id = request.POST.get("obj_id")
        
        # Validaciones básicas
        if action not in ("create", "update", "delete"):
            return JsonResponse({"error": "Acción no válida"}, status=400)
        
        if obj_name not in ["Header", "Banner"]:
            return JsonResponse({"error": "Tipo de objeto no válido"}, status=400)
        
        if action != "create" and (not obj_id or not obj_id.isdigit()):
            return JsonResponse({"error": "ID de objeto no válido"}, status=400)

        try:
            # Modelos disponibles
            objects_dict = {
                "Header": HeaderImages,
                "Banner": BannerImages
            }
            # Validación del tipo de objeto
            if obj_name not in objects_dict:
                return JsonResponse({"error": "Tipo de objeto no válido"}, status=400)
            
            # recuperamos el objeto imagen que queremos modificar
            model_class = objects_dict[obj_name]
            
            # Intentamos recuperar o crear el modelo que trajimos
            if action in ("delete", "update"):
                try:
                    object_image = model_class.objects.get(id=obj_id)
                except model_class.DoesNotExist:
                    return JsonResponse({"error": f"{obj_name} no encontrado"}, status=404)
                
            elif action == 'create':
                store = Store.objects.filter(id=1).first()
                object_image = model_class.objects.create(store=store)
                
            # realizamos el orm que corresponda el DB
            if action == "delete":
                object_image.delete()
                
            # actions ( edit , create )
            else:
                object_image.main_image = main_image
                object_image.soft_delete = soft_delete
                
                # solo guardar en caso de subir imagen
                if request.FILES.get("image"):
                    object_image.image_url = utils.get_url_from_imgbb(request)
                    
            object_image.save()
            tab_html = utils.get_first_tab_render(request)
                
            return JsonResponse({
                "action": action,
                "tab_html": tab_html,
                "image_id": object_image.id,
                "image_url": object_image.image_url
            }, status=201)
            
        except Exception as e:
            return JsonResponse({
                "error": f"Error interno del servidor: {str(e)}"
            }, status=500)            

    # Cuando el request es otro metodo que no sea post    
    return JsonResponse({"error": "Método no permitido"}, status=405)









from home.models import Store, HeaderImages, BannerImages
from orders.models import ShipmentMethod, PaymentMethod, StatusOrder
from users.models import CustomUser
from django.db.models import Prefetch

def profile_page(request):
    user = request.user
    
    # Si no está autenticado, redirigir al home
    if not user.is_authenticated:
        return redirect('/')

    # Verificar si es admin o superadmin
    if user.id == 1 or user.role == 'admin':
        
        # Obtener el store con prefetch optimizado
        store = Store.objects.prefetch_related(
            Prefetch('headers', 
                queryset=HeaderImages.objects.filter(soft_delete=False),
                to_attr='active_headers'
            ),
            Prefetch('headers',
                queryset=HeaderImages.objects.filter(soft_delete=True),
                to_attr='inactive_headers'
            ),
            Prefetch('banners',
                queryset=BannerImages.objects.filter(soft_delete=False),
                to_attr='active_banners'
            ),
            Prefetch('banners',
                queryset=BannerImages.objects.filter(soft_delete=True),
                to_attr='inactive_banners'
            )
        ).filter(id=1).first()
        
        shipments = ShipmentMethod.objects.all()
        payments = PaymentMethod.objects.all()
        users = CustomUser.objects.all()

        # Pasar los datos al contexto para el template
        context = {
            # Listas ya filtradas en el prefetch mejor performance
            'headers_active': store.active_headers,  
            'headers_inactive': store.inactive_headers,
            'banners_active': store.active_banners,
            'banners_inactive': store.inactive_banners,
            'users': users,
            'shipments': shipments,
            'payments': payments
        }
        
        return render(request, 'users/admin_profile.html', context)

    # User Profile Comun
    return render(request, 'users/profile.html')


def register_user(request):
    context = {'provinces': PROVINCIAS_CHOICES}
    return render(request, 'users/register_user.html', context)


def profile_tab(request, tab_name):
    """ 
    cada condicion devuelve de forma asincrona mediante un fetch el html renderizado ademas de un javascript
    asociado para poder utilizar en la pagina
    """
    
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'Tab not found'}, status=404)
    
    
    if tab_name == 'first-tab':
        user = request.user
        # Trae órdenes junto con la factura en una sola consulta SQL
        
        if user.is_superuser:    # verificamos si es admin
            orders = Order.objects.all()
        else:
            orders = user.orders.select_related("invoice").all()
        
        context = { 'orders': orders }
        html_content = render_to_string('users/tabs/pedidos.html', context)
        return JsonResponse({'html': html_content})
        

    if tab_name == 'second-tab':
        favorites = user.favorites.select_related('product').all()
        context = {
            'products': [f.product for f in favorites],
            'favorite_product_ids': {f.product_id for f in favorites}
        }
        return JsonResponse({
            'html': render_to_string('users/tabs/favorites.html', context)
        })


    if tab_name == 'third-tab':
        
        context = {"none": None}
        
        html_content = render_to_string('users/tabs/compras.html', context)
        
        return JsonResponse({'html': html_content})


    return JsonResponse({'error': 'Tab not found'}, status=404)






