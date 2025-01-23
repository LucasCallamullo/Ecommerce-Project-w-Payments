from django.db import models

# Create your models here.

class OrderStatus(models.Model):
    # 1	Cancelado
    # 2	Pendiente
    # 3	Enviado
    # 4	Completado
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
    detail_order = models.TextField(max_length=255, null=True, blank=True)

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
    

class Factura(models.Model):
    f_type = models.CharField(
        max_length=1, 
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C')
        ],
        default="B"
    )
    
    buyer_name = models.CharField(max_length=100, blank=True, null=True)
    buyer_last_name = models.CharField(max_length=100, blank=True, null=True)
    buyer_dni = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cellphone = models.CharField(max_length=15, blank=True, null=True)

    total_items = models.DecimalField(max_digits=10, decimal_places=2)
    shipment_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    invoice_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    name_mp = models.CharField(max_length=100, blank=True, null=True)
    last_name_mp = models.CharField(max_length=100, blank=True, null=True)
    dni_mp = models.CharField(max_length=20, blank=True, null=True)
    
    status = models.CharField(
        max_length=1, 
        choices=[
            ('P', 'Pending'),
            ('A', 'Paid'),
            ('C', 'Cancelled')
        ],
        default='A'
    )

    @property
    def total(self):
        return float(self.total_items + self.shipment_cost - self.discount)

    def __str__(self):
        return f"Factura {self.tipo} - {self.buyer_name} {self.buyer_last_name} - Total: {self.total}"
