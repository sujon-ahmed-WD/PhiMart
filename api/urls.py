from django.urls import path, include, re_path
from product.views import ProductViewSet, CategoryViewSet, ReviewSet, ProductImageViewSet
from order.views import CartViewSet, CartItemViewSet, OrderViewSet, initiate_payment, payment_success, payment_fail, payment_cancel, HasOrderedProduct,stripe_webhook
from rest_framework_nested import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings

# ==== Routers ====
router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet)
router.register('carts', CartViewSet, basename='carts')
router.register('orders', OrderViewSet, basename='orders')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewSet, basename='product_review')
product_router.register('images', ProductImageViewSet, basename='product_image')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-item')

# ==== Swagger Setup ====
schema_view = get_schema_view(
   openapi.Info(
      title="PhiMart hello API",
      default_version='v1',
      description="API documentation",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# ==== URL Patterns ====
urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # path('payment/initiate/', initiate_payment, name='initiate-payment'),
    path('payment/success/', payment_success, name='payment-success'),
    path('payment/fail/', payment_fail, name='payment-fail'),
    path('payment/cancel/', payment_cancel, name='payment-cancel'),
    path('orders/has-ordered/<int:product_id>/', HasOrderedProduct.as_view()),
    path('payment/initiate/',initiate_payment, name='initiate_payment'),
    path('payment/webhook/', stripe_webhook, name='stripe-webhook'),
]

# ==== Swagger URLs only in DEBUG ====
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        
    ]
