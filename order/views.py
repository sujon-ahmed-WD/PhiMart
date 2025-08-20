from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from order.models import Cart,CartItem
from order.serializers import CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer
# Create your views here.
class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
        queryset=Cart.objects.all()
        serializer_class=CartSerializer
        

class CartItemViewSet(ModelViewSet):
        http_method_names=['get','post','patch','delete']
        # serializer_class=CartItemSerializer
        def get_serializer_class(self): # Customize in serializers
                if self.request.method=='POST': 
                        return AddCartItemSerializer
                elif self.request.method=='PATCH':
                        return UpdateCartItemSerializer        
                return CartItemSerializer   # baki time Read kor jono .      
        
        def get_serializer_context(self): # ami serializer cart item dai ni ti akna contex kora dese 
                return{'cart_id':self.kwargs['cart_pk']}     
        
        def get_queryset(self):
                 return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
               # এখানে স্পেসিফিক cart_id অনুযায়ী item গুলো দিবে
