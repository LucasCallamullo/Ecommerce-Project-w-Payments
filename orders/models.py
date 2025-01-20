from django.db import models

# Create your models here.

class OrderStatus(models.Model):
    # [('pendiente', 'Pendiente'), ('enviado', 'Enviado'), ('completado', 'Completado')])
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    
class PaymentMethod(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey('productos.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def subtotal(self):
        return self.quantity * self.price
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='orders')
    status = models.ForeignKey('OrderStatus', on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True)
    envio = models.ForeignKey('Envio', on_delete=models.SET_NULL, null=True)
    factura = models.ForeignKey('Factura', on_delete=models.SET_NULL, null=True)
    at_create = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id} - {self.user.email}"
    

class Envio(models.Model):
    # nombre metodo e info agregada
    method = models.ForeignKey('EnvioMethod', on_delete=models.SET_NULL, null=True)
    
    # para en casos de envios completo
    address = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    detail = models.TextField(max_length=255, null=True, blank=True)
    
    # para casos de retiro en local
    buyer_name = models.CharField(max_length=100, null=True, blank=True)
    buyer_dni = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.method.name if self.method else "Sin método de envío"
    

class EnvioMethod(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return self.name
    

class TipoFactura(models.TextChoices):
    A = 'A', 'A'
    B = 'B', 'B'
    C = 'C', 'C'


class Factura(models.Model):
    tipo = models.CharField(max_length=1, choices=TipoFactura.choices, default=TipoFactura.B)
    buyer_name = models.CharField(max_length=100, blank=True, null=True)
    buyer_dni = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.tipo