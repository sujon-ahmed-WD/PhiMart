from rest_framework import serializers
from order.models import Cart , CartItem
from product.models import Product
from product.serializers import ProductSerializers


class  SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','price']
        

# class AddCartItemSerializer(serializers.ModelSerializer):
#     product_id=serializers.IntegerField() # customize field 
#     class Meta:
#         model = CartItem
#         fields=['id','product_id','quantity']        
        
#     def save(self,**kwargs):
#         cart_id=self.context['cart_id']
#         product_id=self.validated_data['product_id']
#         quantity=self.validated_data['quantity']
#         try:
#             cart_item = CartItem.objects.get(
#                 cart_id=cart_id, product_id=product_id) 
#             cart_item.quantity += quantity
#             self.instance = cart_item  # instance  mana holo amier bortoman data 
#         except CartItem.DoesNotExist:
#             self.instance = CartItem.objects.create(
#                 cart_id=cart_id, **self.validated_data)
#             return self.instance
#         def validation_product_id(self,value):
#             if not Product.objects.filter(pk=value).exists():
#                 raise serializers.ValidationError(
#                     f"Product with {value} dose not exists "
#                 )
#             return value

 
 # bhi 
 
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]

    def validate_product_id(self, value):  
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Product with id {value} does not exist.")
        return value

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        
        try:
            Cart.objects.only("id").get(id=cart_id)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart does not exist.")

        
        cart_item, created = CartItem.objects.get_or_create(
            cart_id=cart_id, product_id=product_id,
            defaults={"quantity": quantity},
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save(update_fields=["quantity"])

        self.instance = cart_item
        return cart_item

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= CartItem
        fields=['quantity']
       
        
class CartItemSerializer(serializers.ModelSerializer):
    # product_price=serializers.SerializerMethodField(method_name='get_product_price') # step 2  coustom feild pries bosa
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    product=SimpleProductSerializer()
    class Meta:
        model = CartItem
        fields=['id','product','quantity','total_price'] # step 3  ata pora include kora desa 
        
    def get_product_price(self,cart_item): # step one cart_item satha product price bar kora 
        return cart_item.product.price 
    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.price

class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)       
    all_items_pries=serializers.SerializerMethodField(method_name='get_total_price') # all items price gulo sum hova ..                             
    class Meta:
        model=Cart
        fields= ['id','user','items','all_items_pries']

    def get_total_price(self,cart:Cart):
        return sum([item.product.price*item.quantity for item in cart.items.all()]) # ata list summentions korsa 