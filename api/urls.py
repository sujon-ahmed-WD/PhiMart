from django.urls import path,include
# from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet,CategoryViewSet,ReviewSet
from order.views import CartViewSet,CartItemViewSet,OrderViewSet
from rest_framework_nested import routers


router=routers.DefaultRouter()
router.register('products',ProductViewSet,basename='products')
router.register('categories',CategoryViewSet),
router.register('carts',CartViewSet,basename='carts')
router.register('orders',OrderViewSet,basename='orders')

product_router=routers.NestedDefaultRouter(router,'products',lookup='product') # 'products' MAIN FIELD   con lookup
product_router.register('reviews',ReviewSet,basename='product_review')

cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',CartItemViewSet,basename='cart-item')

# akna syntax holo 
"""
variable_name=routers.NestedDefaultRouter(router,'parant url',lookup='parant modda ke dea sarch korbo')
variable_name.register('child url',view modda ja file name ja view create korsi tah debo , basebam='readable name')
"""

# urlpatterns = router.urls  # then url setup deva 

urlpatterns = [
    path('',include(router.urls)),
    path('',include(product_router.urls)),
    path('',include(cart_router.urls)),
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
]

 