from rest_framework import serializers
from decimal import Decimal
from product.models import Category,Product,Review
from django.contrib.auth import get_user_model


class CategoriesSerializers(serializers.ModelSerializer):
    product_count=serializers.IntegerField(read_only=True)
    class Meta:
        model= Category
        fields=['id','name','description','product_count']
        


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
    # def create(self,validated_data):
    #     product= Product(**validated_data)
    #     product.other=1
    #     product.save()
    #     return product 
class SimpleUserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(method_name='get_current_user_name')
    class Meta:
        model=get_user_model()
        fields=['id','name']
        
    def get_current_user_name(self,obj):
        return obj.get_full_name()
        
    
    
    
class ReviewSerializers(serializers.ModelSerializer):
        user=SimpleUserSerializer(read_only=True)
        class Meta:
            model=Review
            fields=['id','user','product','ratings','comment']
            read_only_fields=['user','product']
        def create(self, validated_data):
         product_id = self.context['product_id'] #  Catch korbo context data 
         return Review.objects.create(product_id=product_id, **validated_data)