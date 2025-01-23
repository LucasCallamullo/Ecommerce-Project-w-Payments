

from cart.models import Cart, CartItem
from productos.models import Product

from django.utils import timezone
from django.utils.dateparse import parse_datetime


class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        self.carrito = self.session.get("carrito", {})
        self.cart_id = self.session.get("cart_id", None)
        self.last_modified = self.session.get('last_modified', None)
        
        # Logica para manejar sincronizacion entre carritos de disintas pestañas, sesiones
        if request.user.is_authenticated:
            
            # Esto se dara post logeo realmente, porque recien ahi tendra un cart_id
            if self.cart_id:
                # recuperramos Cart con el realted_name
                cart = self.request.user.carrito     
                
                # Compara la fecha de la última modificación
                last_modified = parse_datetime(self.last_modified)
                if cart.last_modified > last_modified:
                    self.cart_id = self.migrate_carrito_to_cart_db(cart=cart)

            # Cuando el cart_id is None, solo ocurre una vez antes de logearse
            else: 
                # recupera los datos desde la base de datos
                self.migrate_carrito_to_cart_db(user=request.user)

        # Si no esta autenticado el usuario no manejamos la base de datos
        else:  # Si se deslogea no accede al Cart que estaba asociado antes
            if self.cart_id is not None:
                self.cart_id = None
                self.session["cart_id"] = self.cart_id
                self.session.modified = True
                
                self.last_modified = None
                self.session['last_modified'] = None
                self.session.modified = True


    # ======================================================================
    #                   Methods n properties
    # ======================================================================
    def migrate_carrito_to_cart_db(self, user=None, cart=None):
        """
            Migra el carrito de la sesión al carrito de base de datos cuando el usuario se registra.
        """
        if cart is None:
            cart, _ = Cart.objects.get_or_create(user=user)
            # Esto se realiza para lograr la sincronizacion entre distintas pestañas
            self.session['last_modified'] = timezone.now().isoformat()
            self.session.modified = True
            
        # obtenemos un diccionario para combinar con el self.carrito de la sesion si existiera
        new_carrito = self.get_carrito_from_cart(cart)
        
        # combinamos ambos carritos o se deolvera el anterior carrito creado de no existir self.carrito
        self.carrito = self.combine_carritos(cart, new_carrito)

        # Guardamos el carrito actualizado datos en la sesión
        self.cart_id = cart.id
        self.session["cart_id"] = self.cart_id
        self.session.modified = True
  
        self.save()
        
    
    def combine_carritos(self, cart, new_carrito):
        """
        logica aplicada para optimizar la consultas realizadas a la db de una vez en vez de una cada vuelta
        product_ids (list): lista por comprension que almacena valores numeros de id
        products (queryset): que almacena los Product filtrados por los valores de la lista
        products_dict (dict): por comprension que almacena al id como key, y el Product como value 
            para acceder despúes a los atributos del modelo

        Args:
            cart (Cart): modelo de la clase Cart de la app cart
            new_carrito (dict): obtenido del metodo self.get_carrito_from_cart puede venir cargado o vacio

        Returns:
            dict: el nuevo diccionario que se posicionara como self.carrito = new_carrito
        """
        if self.carrito:
            product_ids = [item["id"] for item in self.carrito.values()]
            products = Product.objects.filter(id__in=product_ids)
            products_dict = {product.id: product for product in products}
        else:
            return new_carrito
            
        for key, item in self.carrito.items():
            
            # verificamos la existencia o disponibilidad directa de los productos
            product = products_dict.get(item["id"])
            if product is None or not product.available:
                continue
            
            # verificamos existencia en stock del producto recuperado del self.carrito sino lo omitimos
            # y no se incluira en el new_carrito
            quantity = item["qty"]
            stock = self.stock_or_available(product, quantity)
            if not stock:
                continue
            
            # si la key esta en new carrito es porque ya existe ese producto y verificamos su cantidad
            if key in new_carrito.keys():
                update_cart_item = True

                # la logica es trataremos de ponerle el mayor de los dos qty
                if new_carrito[key]["qty"] > item["qty"]:
                    quantity = new_carrito[key]["qty"]
                    update_cart_item = False
                    # se puede usar directamente este porque ya viene del anterior 
                    # ciclo( cart.items.all(): ) la disponibilidad
                    
                # actualizamos valores de cantidad segun haya quedado algun valor
                new_carrito[key]["qty"] = quantity
                
            else:
                # agregamos el nuevo item al carrito 
                update_cart_item = True
                new_carrito[key] = {
                    "id": product.id,
                    "name": product.name,
                    "price": float(product.price),
                    "image": product.main_image,
                    "qty": quantity,
                }
               
            # la bandera se utiliza para evitar consultas innecesarias si no se hicieron cambios en la 
            # quantity de un producto
            if update_cart_item:
                cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
                cart_item.quantity = quantity
                cart_item.save()

        return new_carrito
    
    
    def get_carrito_from_cart(self, cart):
        """
        Recupera todos los items guardados en la db, y los transforma al diccionario que utiliza
        el self.carrito
        
        Estructura del self.carrito:
            self.carrito = {
                "1": {
                    "id": 1,
                    "name": "Product 1",
                    "price": 20.99,
                    "image": "image_url_1.jpg",
                    "qty": 2,
                },
            }
        
        Args:
            cart: modelo Cart de la app cart
        
        Returns:
            un diccionario adaptado al formato del self.carrito de la session que utiizamos,
            lo devolverá vacío o cargado segun contenga o no items
        """
        new_carrito = {}
        for item in cart.items.all():
            
            # recuperamos el objeto producto con todos sus atributos
            product = item.product
            quantity = item.quantity
            
            # consultamos disponibilidad
            stock = self.stock_or_available(product, quantity)
            
            if not stock:
                # probablemente despues agregar alguna logica para avisar que el producto
                # se quedo sin stock o se quito o algo
                cart.update_cart_db(product, action='remove')
                continue
            
            new_carrito[str(product.id)] = {
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "image": product.main_image,
                "qty": quantity,
            }
            
        return new_carrito

    
    def stock_or_available(self, product, qty):
        """_summary_

        Args:
            producto (Product): modelo de la app Productos 
            qty (int): cantidad a consultar disponibilidad en stock

        Returns:
            bool: que nos sirve para saber si podemos realizar una accion que amerite la respuesta en
             True de este metodo
        """
        stock = product.stock if product.available else 0
        
        if stock == 0:
            # Si no hay stock, desactivamos el producto (borrado lógico)
            product.available = False
            product.save()
            return False
    
        quantity = qty
        producto_id_str = str(product.id)
        
        # Comprobar si la clave existe en el diccionario
        if self.carrito:
            if producto_id_str in self.carrito:
                quantity += self.carrito[producto_id_str]["qty"]
    
        if stock < quantity:
            return False
        
        # si no se quedo antes retorna directamente True asumiendo que hay stock
        return True
    
    
    @property
    def total_price(self):
        """
        Notes:
            - Se añade el atributo self.total para realizar el calculo solo una vez mediante
            el context_processors.py, y despues pasarlo como contexto
        """
        total = 0
        if self.carrito:
            total = sum(item['price'] * item['qty'] for item in self.carrito.values())
        return float(total)
    
    
    @property
    def total_items(self):
        total_productos = 0
        if self.carrito:
            total_productos = sum(item['qty'] for item in self.carrito.values())
        return total_productos
        
        
    @property
    def items(self):
        """
        Notes:
            Devuelve el diccionario con formato key, value para poder utilizarlo en las vistas de django
        """
        return self.carrito.items()


    # ======================================================================
    #                   CRUD ACTIONS CARRITO
    # ======================================================================
    def save(self):
        """
            Guarda el carrito en la sesión y sincroniza con la base de datos si es necesario.
        """
        self.session["carrito"] = self.carrito
        self.session.modified = True
        
    
    def handle_cart_to_db(self, product=None, action="", quantity=0):
        """
            Metodo del carrito session encargado de administrar las distintas acciones a realizar
            para el guardado dentro de la base de datos en el modelo de Cart
        """
        try:
            # Obtener el carrito directamente desde el usuario usando la relación inversa
            cart = self.request.user.carrito
            cart.update_cart_db(product=product, action=action, quantity=quantity)
            
            # Esto se realiza para lograr la sincronizacion entre distintas pestañas
            self.session['last_modified'] = timezone.now().isoformat()
            self.session.modified = True
            
        except Cart.DoesNotExist:
            return None  
    

    def add_product(self, product, qty=1) -> bool:
        """
        Agrega un producto al carrito (sesión y base de datos).
        
        Returns:
            bool: retorna un bool para verificaciones cuando se llama esta funcion
        """
        if not self.stock_or_available(product, qty):
            return False
        
        product_id_str = str(product.id)

        # Actualiza el carrito en sesión
        if product_id_str not in self.carrito:
            self.carrito[product_id_str] = {
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "image": product.main_image,
                "qty": qty,
            }
        else:
            self.carrito[product_id_str]["qty"] += qty

        self.save()

        # Actualiza el carrito en la base de datos
        if self.request.user.is_authenticated and self.cart_id:
            quantity = self.carrito[product_id_str]["qty"]
            self.handle_cart_to_db(product=product, action='add', qty=quantity)
            
        return True


    def subtract_product(self, product, qty=1) -> bool:
        """
        Reduce la cantidad de un producto del carrito.
        Al final retornara un bool que nos servira para indicar distintos tipo de mensajes
        segun la peticion ajax realizadas en views.py
        """
        product_id_str = str(product.id)
        
        # Convertir el ID del producto a cadena de texto
        if self.carrito[product_id_str]["qty"] > 1:
            self.carrito[product_id_str]["qty"] -= qty
            delete_item = False
        else:
            # Opcionalmente, podemos eliminar el producto si la cantidad llega a 0
            del self.carrito[product_id_str]
            delete_item = True
        
        # actualizar la base de datos desde el modelo en la app cart
        if self.request.user.is_authenticated and self.cart_id:
            self.handle_cart_to_db(product=product, action='substract', quantity=qty)
            
        # guardamos los cambios en el carrito de la session
        self.save()
        
        # este retorno nos sirve para los mensajes de las alertas
        return delete_item


    def remove_product(self, product) -> bool:
        """
            Elimina un producto del carrito.
            No se realizan verificaciones de las key debido a que la logica no permitiría 
            que sucedieran
        """
        product_id_str = str(product.id)
        del self.carrito[product_id_str]
        self.save()

        # guardamos los cambios en la base de datos si el usuario es autenticado
        if self.request.user.is_authenticated and self.cart_id:
            self.handle_cart_to_db(product=product, action='remove')
            
        # este retorno nos sirve para los mensajes de las alertas
        return True

    
    def clear(self):
        """
            Limpia el carrito.
        """
        self.carrito = {}
        self.save()
        
        # guardamos los cambios en la base de datos si el usuario es autenticado
        if self.request.user.is_authenticated and self.cart_id:
            self.handle_cart_to_db(action='clear')
