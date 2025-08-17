from django.urls import path
from product import views



urlpatterns = [
    path('',views.ProductViewSet.as_view(),name='view_products'),
    path('<int:id>/', views.ProductList.as_view(), name='view_product'),
]

