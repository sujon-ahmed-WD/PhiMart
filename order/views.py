from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
import stripe
from order.models import Cart,CartItem,Order
from order.serializers import CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,OrderSerializer,CreateOrderSerializer,UpdateOrderSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from order import serializers as orderSz
from rest_framework.decorators import action
from order.services import OrderService 
from rest_framework.decorators import api_view
from sslcommerz_lib import SSLCOMMERZ  
from django.conf import settings as main_settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from .models import OrderItem
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
        def create(self,request,*args, **kwargs):
                existing_cart =Cart.objects.filter(user=request.user).first()

                if existing_cart:
                        serializer=self.get_serializer(existing_cart)
                        return Response(serializer.data,status=status.HTTP_200_OK)
                return super().create(request,*args,**kwargs)
        

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
    http_method_names = ['get', 'post', 'delete', 'patch', 'head', 'options']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user=request.user)
        return Response({'status': 'Order canceled'})

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = orderSz.UpdateOrderSerializer(
            order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f'Order status updated to {request.data['status']}'})

    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'cancel':
            return orderSz.EmptySerializer
        if self.action == 'create':
            return orderSz.CreateOrderSerializer
        elif self.action == 'update_status':
            return orderSz.UpdateOrderSerializer
        return orderSz.OrderSerializer

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user': self.request.user}

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)

# ------------------------SSL Comaraze-----------------------------------------------
@api_view(['POST'])
def initiate_payment(request):
    user=request.user
    amount=request.data.get("amount")
    order_id=request.data.get("orderId")
    num_items=request.data.get("numItems")
    settings = { 'store_id': 'phima69077fbf2c24a', 'store_pass': 'phima69077fbf2c24a@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"txn_{order_id}"
    post_body['success_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/success/"
    post_body['fail_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/fail/"
    post_body['cancel_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = "cus_phone"
    post_body['cus_add1'] = user. address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = num_items
    post_body['product_name'] = "E-commerce Products"
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    # print(response)
    
    if response.get('status')=='SUCCESS':
        return Response({"payment_url":response['GatewayPageURL']})
    return Response({"error":"Payment initiation failed"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def payment_success(request):
    # print("transaction_Id",request.data.get("tran_id"))
    print("Inside success")
    order_id = request.data.get("tran_id").split('_')[1]
    order = Order.objects.get(id=order_id)
    order.status = "Ready To Ship"
    order.save()
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")
@api_view(['POST'])
def payment_fail(request):
        return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")

@api_view(['POST'])

def payment_cancel(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")
    


class HasOrderedProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        user = request.user
        has_ordered = OrderItem.objects.filter(
            order__user=user, product_id=product_id).exists()
        return Response({"hasOrdered": has_ordered})


#---------------------Strip-------------------------------

stripe.api_key = main_settings.STRIPE_SECRET_KEY  # তোমার Stripe secret key

@api_view(['POST'])
def initiate_payment(request):
    user=request.user
    amount=request.data.get("amount")
    order_id=request.data.get("orderId")
    num_items=request.data.get("numItems")

    # Stripe expects amount in paisa (ছোট একক)
    stripe_amount = int(float(amount) * 100)  # যেমন 500.50 BDT -> 50050 paisa

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'E-commerce Products',
                    },
                    'unit_amount': stripe_amount,
                },
                'quantity': int(num_items),
            }],
         
         
     
            mode='payment',
            success_url=f"{main_settings.FRONTEND_URL}/dashboard/orders/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{main_settings.FRONTEND_URL}/dashboard/orders/",
            metadata={
                "order_id": order_id,
                "user_id": user.id
            }
        )
        return Response({"payment_url": checkout_session.url})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = main_settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return Response(status=400)
    except stripe.error.SignatureVerificationError:
        return Response(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['metadata']['order_id']
        try:
            order = Order.objects.get(id=order_id)
            order.status = "Ready To Ship"
            order.save()
        except Order.DoesNotExist:
            pass

    return Response(status=200)