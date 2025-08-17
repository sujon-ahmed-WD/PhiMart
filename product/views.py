from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category
from product.serializers import ProductSerializers,CategoriesSerializers
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

# Genric_view_ ..................
class ProductViewSet(ModelViewSet): # this is modelviewset
    queryset=Product.objects.all()
    serializer_class=ProductSerializers

    def destroy(self, request, *args, **kwargs): # ata modelviewsetup customize korsa
        product = self.get_object()
        if product.stock > 10:
            return Response({'message': "Product with stock more than 10 could not be deleted"})
        self.perform_destroy(product) # save korsa ata .....
        return Response(status=status.HTTP_204_NO_CONTENT)

     
    
class CategoryViewSet(ModelViewSet): # --------> this is model_view_Set
    queryset=Category.objects.annotate(
        product_count=Count('products')).all()
    serializer_class=CategoriesSerializers
    
    

      