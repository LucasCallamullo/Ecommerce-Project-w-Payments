


# serializers.py
from rest_framework import serializers
from django.utils.text import slugify


from products.models import Product, PCategory, PSubcategory, PBrand, ProductImage
from products import utils


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer para validar y actualizar productos.
    Espera datos como:
    {
        "name": "Nombre del producto",
        "price": "30.000",
        "discount": "20",
        "stock": "1",
        "available": true,
        "description": "<p>Descripción HTML</p>",
        "category": 2,
        "subcategory": 6,
        "brand": 5,
        "main_image": 20
    }
    """
    
    # cuando queres aplicar logica personalizada a atributos de tu modelo, DEBES reemplazar
    # su valor aceptado por el que prefieras ( en este caso DECIMAL_FIELD y URL_FIELD aceptan STR)
    price = serializers.CharField()
    
    # utilizamos esta forma para personalizar las entradas y salidas de relaciones fk o manytomany
    main_image = serializers.CharField(required=False, allow_null=True)
    category = serializers.CharField(required=False, allow_null=True)    # Permite '0' para setear a None
    subcategory = serializers.CharField(required=False, allow_null=True)
    brand = serializers.CharField(required=False, allow_null=True)
    
    def to_representation(self, instance):
        # 1. Call the original method to get the default serialized data as a dictionary.
        representation = super().to_representation(instance)
        
        # 2. Replace specific fields with human-readable names.
        # For example, instead of returning an ID for 'category', return its name.
        representation['main_image'] = instance.main_image if instance.main_image else None
        representation['category'] = instance.category.name if instance.category else None
        representation['subcategory'] = instance.subcategory.name if instance.subcategory else None
        representation['brand'] = instance.brand.name if instance.brand else None
        
        # 3. Return the updated dictionary as the final serialized output.
        return representation
    
    class Meta:
        model = Product
        fields = [
            'name', 'price', 'stock', 'available', 'description', 'discount', 
            'main_image', 'category', 'subcategory', 'brand'
        ]

    def validate_category(self, value):
        # Tomar en cuenta que esta validación funciona y las subsecuentes relaciones de FK hacen esto
        # Pese a ser una relacion fk, en drf pedimos el valor como str y hacemos nuestra propia validacion
        
        # 1. Valuamos el STR que llega desde el front/json que se un INT positivo
        value = utils.valid_id_or_None(value)  # Convierte '0' en None
        if not value: # La lógica de esto que desde el front mandamos un 0 para quitar la Category asociada permitiendo null
            return None
        
        # 2. Optimniza retornar una fk directa sin hacer consulta extra
        if self.instance and getattr(self.instance, 'category_id', None) == value:
            return self.instance.category # PCategory(id=value)
        
        # 3. Si en cuentra una categoría valida directamente devuelve el "Objeto" y lo asocia como FK
        try:
            return PCategory.objects.get(id=value)
        # 4. En este caso si intenta asociar una Categoria que no existe devuelve un error y cancela la operacion ( ver response )
        except PCategory.DoesNotExist:
            raise serializers.ValidationError("La categoría no existe.")

    def validate_brand(self, value):
        value = utils.valid_id_or_None(value)  # Convierte '0' en None
        if not value:
            return None
        # 2. Optimniza retornar una fk directa sin hacer consulta extra
        if self.instance and getattr(self.instance, 'brand_id', None) == value:
            return self.instance.brand # PBrand(id=value)
        try:
            return PBrand.objects.get(id=value)
        except PBrand.DoesNotExist:
            raise serializers.ValidationError("La marca no existe.")

    def validate_subcategory(self, value):
        # obtiene el STR de la category anterior validadandola
        value = utils.valid_id_or_None(value)  # Convierte '0' en None
        category_id = utils.valid_id_or_None(self.initial_data.get("category"))
        
        # 1. No se puede validar subcategoría si no hay categoría válida asociada
        if None in (value, category_id):
            return None
        # 2. Validar coherencia de category con la subcategory retornar directo si no hubo cambios
        if self.instance and getattr(self.instance, 'category_id', None) == category_id: 
            if getattr(self.instance, 'subcategory_id', None) == value:
                return self.instance.subcategory # PSubcategory(id=value)
        # 3. Para en caso que eligiera una nueva validar que sea correcta su categoria filtramos 
        # por su fk_field
        try:
            return PSubcategory.objects.get(id=value, category_id=category_id)
        except PSubcategory.DoesNotExist:
            raise serializers.ValidationError("La subcategoría no existe.")
        
    def validate_stock(self, value):
        """
        Valida que el stock sea un número entero mayor o igual a 0.
        """
        return utils.parse_number(value, "Stock", allow_zero=True)
    
    def validate_discount(self, value):
        """
        Valida que el descuento sea un número entero mayor o igual a 0.
        """
        return utils.parse_number(value, "Descuento", allow_zero=True)

    def validate_price(self, value):
        """
        Valida que el precio sea un número flotante mayor que 0.
        """
        return utils.parse_number(value, "Precio", allow_zero=False)
    
    def validate_main_image(self, value):
        """
        Valida que la nueva url exista y sea del producto y asocia la nueva imagen, tambien viene como STR (ver Category).
        """
        value = utils.valid_id_or_None(value)
        if not value:
            return None
        
        # 1. accedemos al prefetch queryset que ya viene de antes del producto
        for image in self.instance.images_all:

            # 2. encontramos la imagen a actuailizar y llamamos al metodo de ProductImage
            if image.id == value:
                image.update_main_image(self.instance.images_all)
                return image.image_url

        return None    # 3. si por algun motivo falla retornamos none

    def validate_available(self, value):
        """
        Asegura que el campo 'available' sea booleano válido,
        incluso si llega como string desde el front.
        """
        if isinstance(value, str):
            value = value.lower()
            if value == "true":
                return True
            elif value == "false":
                return False
            else:
                raise serializers.ValidationError("El valor de 'available' debe ser 'true' o 'false'.")
        elif isinstance(value, bool):
            return value
        else:
            raise serializers.ValidationError("El campo 'available' debe ser booleano.")
        
    def validate_name(self, value):
        # Solo validamos 'name' para evitar actualizar slug y normalized_name si no cambia.
        # El resto de campos se actualiza siempre (no afecta lógica interna ni rendimiento).
        if len(value) <= 2:
            raise serializers.ValidationError("El campo 'name' debe tener una extension minima de 3 letras.")
        
        if self.instance.name != value:
            return value
        return None
    
    def validate_description(self, value):
        """
        Sanitiza el contenido HTML recibido en el campo 'description'.
        """
        return utils.sanitize_html(value)
            
    def update(self, instance, validated_data):
        # Imprimir todas las claves y valores de validated_data
        print("Contenido de validated_data:")
        for key, value in validated_data.items():
            print(f"{key}: {value}")
        
        # 1 - solo dejar modificar ciertos campos a un vendedor , se pasa desde la views el context
        user = self.context['user']
        if user.role == 'seller':
            # 2 - Restringimos campos que no puede modificar el vendedor
            removed = []
            for field in ['price', 'stock', 'price_list', 'discount']:
                if field in validated_data:
                    validated_data.pop(field)
                    removed.append(field)
            if removed:
                print(f"Seller intentó modificar campos restringidos: {removed}")
            # 3 - Terminamos el update parcial con los campos que queden en validated_data
            return super().update(instance, validated_data)

        # 1. Procesar 'name' si es un nuevo value antes del update
        new_name = validated_data.get("name")
        if new_name:
            validated_data["normalized_name"] = utils.normalize_or_None(new_name)
            validated_data["slug"] = slugify(new_name)
        # 1b. en caso de recuperar un None ( es decir sin cambios ) eliminamos del update
        else:
            validated_data.pop("name", None)

        # 2. Hacer el update con todos los campos, incluido 'name', si vino
        return super().update(instance, validated_data)









class ProductImageSerializer(serializers.ModelSerializer):
    """Serializador para ProductImage."""
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'main_image']


class PCategorySerializer(serializers.ModelSerializer):
    """Serializador para PCategory."""
    
    class Meta:
        model = PCategory
        fields = ['id', 'name']


class PSubcategorySerializer(serializers.ModelSerializer):
    """Serializador para PSubcategory."""
    
    class Meta:
        model = PSubcategory
        fields = ['id', 'name']


class PBrandSerializer(serializers.ModelSerializer):
    """Serializador para PBrand."""
    
    class Meta:
        model = PBrand
        fields = ['id', 'image', 'image_url']


class ProductListFilters(serializers.ModelSerializer):
    """Serializador para Product."""
    
    # Relaciones explicitas con el Foreign Key
    # brand = PBrandSerializer()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'stock', 'stars', 
            'slug', 'main_image', 'calc_discount'
        ]



