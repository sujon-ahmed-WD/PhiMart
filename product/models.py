from django.db import models
from django.conf import settings
from django.core .validators import MaxValueValidator, MinValueValidator
from product.validators import validate_file_size

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    stock = models.PositiveIntegerField(default=0)  
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image= models.ImageField(upload_to='products/images/',validators=[validate_file_size])
     # file = models.FileField(upload_to="product/files",
    #                         validators=FileExtensionValidator(['pdf'])) ata file format pictuer


class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    # name=models.CharField(max_length=150)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    comment=models.TextField()
    ratings=models.PositiveBigIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    
    
    def __str__(self):
        return f"Review by{self.user.first_name} on{self.product.name}"



# step in build in api
#model
# Serializer
#viewSetup
#router    