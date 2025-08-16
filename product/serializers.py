from rest_framework import serializers
from decimal import Decimal
from product.models import Category,Product


class CategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields=['id','name','description','product_count']
        
    product_count=serializers.IntegerField()


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields=['id','name','description','price','stock','category','price_with_tex']
        
    price_with_tex=serializers.SerializerMethodField(method_name='calculate_tex')
    
    def calculate_tex(self,product):
        return round(product.price*Decimal(1.1),2)
    
    def validate_price(self, price): # field validation
        if price < 0:
            raise serializers.ValidationError('Price could not be negative')
        return price
    
    
    #------------ this is update method----------#                           
    def create(self,validated_data):
        product= Product(**validated_data)
        product.other=1
        product.save()
        return product 