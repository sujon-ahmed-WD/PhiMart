from django.urls import path,include
# from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet,CategoryViewSet,ReviewSet,ProductImageViewSet
from order.views import CartViewSet,CartItemViewSet,OrderViewSet,initiate_payment,payment_success,payment_fail,payment_cancel,HasOrderedProduct
from rest_framework_nested import routers


router=routers.DefaultRouter()
router.register('products',ProductViewSet,basename='products')
router.register('categories',CategoryViewSet),
router.register('carts',CartViewSet,basename='carts')
router.register('orders',OrderViewSet,basename='orders')


product_router=routers.NestedDefaultRouter(router,'products',lookup='product') # 'products' MAIN FIELD   con lookup
product_router.register('reviews',ReviewSet,basename='product_review')
product_router.register('images',ProductImageViewSet,basename='product_image')
cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',CartItemViewSet,basename='cart-item')

# akna syntax holo 
"""
variable_name=routers.NestedDefaultRouter(router,'parant url',lookup='parant modda ke dea sarch korbo')
variable_name.register('child url',view modda ja file name ja view create korsi tah debo , basebam='readable name')
"""

# urlpatterns = router.urls  # then url setup deva 
# 
urlpatterns = [
    path('',include(router.urls)),
    path('',include(product_router.urls)),
    path('',include(cart_router.urls)),
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path('payment/initiate/',initiate_payment,name='initiate-payment'),
    path('payment/success/',payment_success,name='payment-success'),
    path('payment/fail/',payment_fail,name='payment-fail'),
    path('payment/cancel/',payment_cancel,name='payment-cancel'),
    path('orders/has-ordered/<int:product_id>/',
         HasOrderedProduct.as_view())
]

 