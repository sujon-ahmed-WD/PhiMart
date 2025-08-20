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
    PENDING ='pending'
    SHIPPED = 'shipped'
    DELIVERED='delivered'
    STATUS_CHOICES=[
        (PENDING,'pending'), # bam pas holo database and dan pas holo admin panel
        (SHIPPED,'shipped'),
        (DELIVERED,'delivered')
    ]
    user=models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
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
    
    def __str__(self):
        return f"{self.quality} of {self.product.name} in Order {self.order.id}"