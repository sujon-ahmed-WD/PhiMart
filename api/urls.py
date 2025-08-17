from django.urls import path,include
# akna 1st import korbo DefaultRouter
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet,CategoryViewSet

router=DefaultRouter()
router.register('products',ProductViewSet)
router.register('categories',CategoryViewSet)
# sytanx holo => router.register('kon protocol show kora ta deva ', and konview kaj korsa ta deva )


urlpatterns = router.urls  # then url setup deva 

# urlpatterns=[
#     path('',include(routers.urls)),
#     # akna jodi aro url thka amna use kora jaba 
# ]