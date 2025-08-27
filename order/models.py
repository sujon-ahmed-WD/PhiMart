from django.db import models
from users.models import User
from product.models import Product
from uuid import uuid4
class Cart(models.Model): # add to cart ... .. 
    #http://127.0.0.1:8000/api/v1/carts/1/  agula asla  dela hak bah access korta parva ti  uniq id make korsa ..... 
    id=models.UUIDField(primary_key=True,default=uuid4,editable=False) # unique id desa ... 
    user=models.OneToOneField(
        User,on_delete=models.CASCADE, related_name='cart')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart of {self.user.first_name}"
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE )
    quantity=models.PositiveIntegerField()
    class Meta:
         #item poti addtocard modda akta kora thakva ti uniq_together use korsa
        unique_together=[['cart','product']]#=> syntax:=>  unique_together=[['jar modda thkva ','ke 2 bar thakta parva nh oita debo ']]  
    
    # class Meta:
    #  constraints = [
    #     models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product') recommenced in django 
    # ]
    
    def __str__(self): # Reptasion jono 
        return f"{self.quantity} of {self.product.name}"    
    

class Order(models.Model):
    NOT_PAID ='Not paid'
    READY_TO_SHIP = 'Ready to ship'
    SHIPPED = 'shipped'
    DELIVERED='delivered'
    CANCELED='canceled'
    STATUS_CHOICES=[
        (NOT_PAID,'Not paid'), # bam pas holo database and dan pas holo admin panel
        (SHIPPED,'Shipped'),
        (READY_TO_SHIP,'Ready to ship'),
        (CANCELED,'Canceled'),
        (DELIVERED,'Delivered')
    ]
    user=models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    id=models.UUIDField(primary_key=True,default=uuid4,editable=False) #  unique id desa ... 
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_PAID)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(
        Order,on_delete=models.CASCADE, related_name='items'  
    )
    product=models.ForeignKey(
        Product, on_delete=models.CASCADE
    )
    quality=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    total_price=models.DecimalField(max_digits=12,decimal_places=2)
    
    def __str__(self):
        return f"{self.quality} of {self.product.name} in Order {self.order.id}"