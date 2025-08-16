from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category
from product.serializers import ProductSerializers,CategoriesSerializers
from django.db.models import Count




@api_view(['GET','POST']) 
def view_products(request):
    if request.method=='GET':
        products=Product.objects.select_related('category').all()  # ae line sob ok
         # akna meny holo onke product ti and contex holo request data devo 
        serializer=ProductSerializers(products,many=True)
        return Response(serializer.data)
    
    if request.method=='POST':
        serializer=ProductSerializers(data=request.data) # DeSerializers mna jason ka object format convert korsa 
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def view_specific_product(request, id):
    if request.method=='GET':
         product =get_object_or_404(Product,pk=id)   
         serializer=ProductSerializers(product)  
         return Response(serializer.data)
    if request.method=='PUT':
        product=get_object_or_404(Product,pk=id)
        serializer=ProductSerializers(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method=='DELETE':
        product=get_object_or_404(Product,pk=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


@api_view()
def view_categories(request):
    categories=Category.objects.annotate(product_count=Count('products')).all()
    serializer=CategoriesSerializers(categories,many=True)
    return Response(serializer.data)


@api_view()
def view_specific_category(request,pk):
    category=get_object_or_404(Category,pk=pk)
    serializer=CategoriesSerializers(category)
    return Response(serializer.data)