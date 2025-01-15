

class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        carrito = self.session.get("carrito")

        if not carrito:
            carrito = self.session["carrito"] = {}

        self.carrito = carrito
        

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
            - Recupera los items del diccionario del carrito para eventualmente recorrerlo de forma
            actualizada
        """
        return self.carrito.items()
    

    def stock_or_available(self, producto, value_add):
        stock = producto.stock if producto.available else 0
        
        if stock == 0:
            return False
    
        quantity = value_add
        producto_id_str = str(producto.id) 
        
        # Comprobar si la clave existe en el diccionario
        if producto_id_str in self.carrito:
            quantity += self.carrito[producto_id_str]["qty"]
    
        if stock < quantity:
            return False
        
        # si no se quedo antes retorna directamente True asumiendo que hay stock
        return True
    

    # ======================================================================
    #                   ADD n LESS Products
    # ======================================================================
    def add_product(self, product, qty):
        # Convertir el ID del producto a cadena de texto para las keys del dict
        producto_id_str = str(product.id)
        
        # Verifica si el producto no está en el carrito para agregarlo
        if producto_id_str not in self.carrito.keys():
            
            # Obtener la imagen principal del producto con su propiedad
            image_url = product.main_image
            
            # Crear item con elementos necesarios
            self.carrito[producto_id_str] = {
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "image": image_url,
                "qty": qty
            }

        # Si el producto ya está en el carrito solo uno a la cantidad
        else:
            # se puede agregar una variable de comparacion con el stock #
            self.carrito[producto_id_str]["qty"] += qty

        self.save()

    def less_producto(self, producto_id):
        # Convertir el ID del producto a cadena de texto
        producto_id_str = str(producto_id)

        if self.carrito[producto_id_str]["qty"] > 1:
            self.carrito[producto_id_str]["qty"] -= 1
            delete_item = False
        else:
            # Opcionalmente, podemos eliminar el producto si la cantidad llega a 0
            del self.carrito[producto_id_str]
            delete_item = True

        # guardamos los cambios
        self.save()
        
        # este retorno nos sirve para los mensajes de las alertas
        return delete_item


    # ======================================================================
    #                   SAVE, CLEAR; DELETE
    # ======================================================================
    def save(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def remove_producto(self, producto_id):
        producto_id_str = str(producto_id)  # Convertir el ID del producto a cadena de texto

        del self.carrito[producto_id_str]
        self.save()

    def clear_producto(self):
        # Todavia no tiene uso en el widget
        self.carrito = {}
        self.save()



