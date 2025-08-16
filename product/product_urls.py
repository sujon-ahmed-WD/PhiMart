from django.urls import path
from product import views


urlpatterns = [
    path('',views.view_products,name='view_products'),
    path('<int:id>/', views.view_specific_product, name='view_product'),
]

