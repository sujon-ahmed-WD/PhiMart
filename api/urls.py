from django.urls import path,include
# from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet,CategoryViewSet,ReviewSet
from rest_framework_nested import routers

router=routers.DefaultRouter()
router.register('products',ProductViewSet,basename='products')
router.register('categories',CategoryViewSet)

# product_router=routers.NestedDefaultRouter(router,'products',lookup='product') # 'products' MAIN FIELD   con lookup
# product_router.register('reviews',ReviewSet,basename='product_view')
 
product_router=routers.NestedDefaultRouter(router,'products',lookup='product') # 
product_router.register('reviews',ReviewSet,basename='product_review')

# urlpatterns = router.urls  # then url setup deva 

urlpatterns = [
    path('',include(router.urls)),
    path('',include(product_router.urls))
]

 