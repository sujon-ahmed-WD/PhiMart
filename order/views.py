from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from order.models import Cart,CartItem,OrderItem,Order
from order.serializers import CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,OrderSerializer,CreateOrderSerializer,UpdateOrderSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
# Create your views here.
class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
        # queryset=Cart.objects.all()
        serializer_class=CartSerializer
        permission_classes=[IsAuthenticated]
        
        def perform_create(self, serializer): # একজন user এর জন্য শুধু একটি cart allow করা হবে
                cart, created = Cart.objects.get_or_create(user=self.request.user)
                self.instance = cart   # যাতে duplicate না হয়
        
        def get_queryset(self):
                return Cart.objects.filter(user=self.request.user)
        

class CartItemViewSet(ModelViewSet):
        http_method_names=['get','post','patch','delete']
        # serializer_class=CartItemSerializer
        def get_serializer_class(self): # Customize in serializers
                if self.request.method=='POST': 
                        return AddCartItemSerializer
                elif self.request.method=='PATCH':
                        return UpdateCartItemSerializer        
                return CartItemSerializer   # baki time Read kor jono .      
        
        def get_serializer_context(self):                 # ami serializer cart item dai ni ti akna contex kora dese 
                return{'cart_id':self.kwargs.get('cart_pk')} 

                
        def get_queryset(self):
                 return CartItem.objects.filter(cart_id=self.kwargs.get('cart_pk'))
               # এখানে স্পেসিফিক cart_id অনুযায়ী item গুলো দিবে

class OrderViewSet(ModelViewSet):
        # queryset=Order.objects.all()
        # serializer_class=OrderSerializer
        # permission_class=[IsAuthenticated]
        http_method_names=['get','post','delete','patch','head','options']
        
        def get_permissions(self):
                if self.request.method in ['PATCH','DELETE']:
                        return [IsAdminUser()]
                return [IsAuthenticated]
        
        def get_serializer_class(self):
                if self.request.method=='POST':  # post in or create order 
                        return CreateOrderSerializer
                elif self.request.method=='PATCH': # order sov update korta hola 
                        return UpdateOrderSerializer
                return OrderSerializer # get / Read korbo  in order 
        
        def get_serializer_context(self):
                return {'user_id':self.request.user.id}
        
        
                
        def get_queryset(self):
            if self.request.user.is_staff:
                return Order.objects.prefetch_related('items__product').all()  # যদি user staff হয় তবে সব order দেখতে পারবে
            return Order.objects.prefetch_related('items__product').filter(user=self.request.user)  # না হলে শুধু নিজের order দেখতে পারবে