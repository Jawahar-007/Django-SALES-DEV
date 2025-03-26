from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class User(AbstractUser):
    pass

class Customer(models.Model):
    name = models.CharField(max_length=252)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    prod_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.prod_name
    
class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        CONFIRMED = "Confirmed"
        CANCELLED = "Cancelled"

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name = 'customer',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,choices=StatusChoices.choices,default=StatusChoices.PENDING)
    products = models.ManyToManyField(Product,through="OrderItem",related_name = 'orders')
    def __str__(self):
        return f"Order {self.order_id} by {self.customer.name}"    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.prod_name} in Order {self.order.order_id}"